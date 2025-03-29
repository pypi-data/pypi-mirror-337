import pandas as pd
import numpy as np
from .Embed import embed_cluster_texts
from indoxArcg.data_loader_splitter.ClusteredSplit.cs_utils import rechunk
from loguru import logger
import sys

# Set up logging
logger.remove()  # Remove the default logger
logger.add(
    sys.stdout, format="<green>{level}</green>: <level>{message}</level>", level="INFO"
)

logger.add(
    sys.stdout, format="<red>{level}</red>: <level>{message}</level>", level="ERROR"
)


def embed_cluster_summarize_texts(
    texts,
    embeddings,
    dim: int,
    threshold: float,
    level: int,
    summary_model,
    re_chunk: bool = False,
    max_chunk: int = 100,
):
    """
    Embeds, clusters, and summarizes a list of texts. This function first generates embeddings for the texts,
    clusters them based on similarity, expands the cluster assignments for easier processing, and then summarizes
    the content within each cluster.

    Parameters:
    - texts: A list of text documents to be processed.
    - embeddings: An object capable of generating embeddings, must have an `embed_documents` method.
    - dim: int, the dimension of the embeddings.
    - threshold: float, the clustering threshold.
    - level: int, an integer parameter that could define the depth or detail of processing.
    - re_chunk: bool, whether to re-chunk the summaries.
    - max_chunk: int, the maximum size of a chunk.

    Returns:
    - Tuple containing two DataFrames:
      1. The first DataFrame (`df_clusters`) includes the original texts, their embeddings, and cluster assignments.
      2. The second DataFrame (`df_summary`) contains summaries for each cluster, the specified level of detail,
         and the cluster identifiers.
    """

    # Embed and cluster the texts, resulting in a DataFrame with 'text', 'embd', and 'cluster' columns
    df_clusters = embed_cluster_texts(texts, embeddings, dim, threshold)

    # Expand DataFrame entries to document-cluster pairings for straightforward processing
    expanded_list = [
        {"text": row["text"], "embd": row["embd"], "cluster": row["cluster"]}
        for index, row in df_clusters.iterrows()
    ]
    for item in expanded_list:
        if isinstance(item["cluster"], np.ndarray):
            item["cluster"] = tuple(item["cluster"])

    # Create DataFrame
    expanded_df = pd.DataFrame(expanded_list)
    # Retrieve unique cluster identifiers for processing
    all_clusters = expanded_df["cluster"].unique()
    logger.info(f"--Generated {len(all_clusters)} clusters--")

    # Summarize the texts in each cluster
    summaries = []
    for cluster in all_clusters:
        cluster_texts = expanded_df[expanded_df["cluster"] == cluster]["text"].tolist()
        summary = summary_model.get_summary(cluster_texts)
        summaries.append(summary)

    # Create a DataFrame to store summaries with their corresponding cluster and level
    df_summary = pd.DataFrame(
        {
            "summaries": summaries,
            "level": [level] * len(summaries),
            "cluster": list(all_clusters),
        }
    )

    if re_chunk:
        df_summary = rechunk(df_summary=df_summary, max_chunk=max_chunk)

    return df_clusters, df_summary


def recursive_embed_cluster_summarize(
    texts,
    embeddings,
    dim: int,
    threshold: float,
    summary_model,
    max_chunk: int = 100,
    level: int = 1,
    n_levels: int = 3,
    re_chunk: bool = False,
    remove_sword: bool = False,
):
    """
    Recursively embeds, clusters, and summarizes texts up to a specified level or until
    the number of unique clusters becomes 1, storing the results at each level using a specified embeddings object.

    Parameters:
    - texts: List[str], texts to be processed.
    - embeddings: An object capable of generating embeddings, must have an `embed_documents` method.
    - dim: int, the dimension of the embeddings.
    - threshold: float, the clustering threshold.
    - max_chunk: int, the maximum size of a chunk.
    - level: int, current recursion level (starts at 1).
    - n_levels: int, maximum depth of recursion.
    - re_chunk: bool, whether to re-chunk the summaries.
    - remove_sword: bool, whether to remove stop words.

    Returns:
    - A tuple containing the results, input tokens, and output tokens.
    """
    if remove_sword:
        from indoxArcg.data_loader_splitter.utils.clean import remove_stopwords_chunk

        texts = remove_stopwords_chunk(texts)

    results = {}

    # Perform embedding, clustering, and summarization for the current level
    df_clusters, df_summary = embed_cluster_summarize_texts(
        texts,
        embeddings,
        dim,
        threshold,
        level,
        summary_model=summary_model,
        re_chunk=re_chunk,
        max_chunk=max_chunk,
    )

    # Store the results of the current level
    results[level] = (df_clusters, df_summary)

    # Determine if further recursion is possible and meaningful
    unique_clusters = df_summary["cluster"].nunique()
    if level < n_levels and unique_clusters > 1:
        new_texts = df_summary["summaries"].tolist()
        next_level_results = recursive_embed_cluster_summarize(
            texts=new_texts,
            summary_model=summary_model,
            embeddings=embeddings,
            dim=dim,
            threshold=threshold,
            max_chunk=max_chunk,
            level=level + 1,
            n_levels=n_levels,
            re_chunk=re_chunk,
            remove_sword=remove_sword,
        )

        results.update(next_level_results)

    return results
