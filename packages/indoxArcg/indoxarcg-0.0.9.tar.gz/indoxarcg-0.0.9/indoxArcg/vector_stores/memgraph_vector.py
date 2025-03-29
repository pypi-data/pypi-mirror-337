from typing import List, Tuple, Callable, Optional
from indoxArcg.core import Document


class MemgraphVector:
    def __init__(
        self,
        uri: str,
        username: str,
        password: str,
        embedding_function: Callable,
        search_type: str = "vector",
    ):
        """
        Initializes the connection to the Memgraph database and sets up the embedding function.

        Args:
            uri (str): URI of the Memgraph instance.
            username (str): Username for Memgraph.
            password (str): Password for Memgraph.
            embedding_function (Callable): The embedding function (e.g., OpenAI, custom model) to convert query text to embeddings.
            search_type (str): Default search type ('vector', 'keyword', or 'hybrid'). Defaults to 'vector'.
        """
        from neo4j import GraphDatabase

        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self._embedding_function = embedding_function
        self.default_search_type = search_type

    def close(self):
        """Closes the Memgraph connection."""
        if self.driver:
            self.driver.close()

    def _similarity_search_with_score(
        self, query: str, k: int = 4, search_type: Optional[str] = None, **kwargs
    ) -> List[Tuple[Document, float]]:
        """
        Run similarity search with scores based on the selected search type.

        Args:
            query (str): The search query.
            k (int): Number of top results to return. Defaults to 4.
            search_type (Optional[str]): The type of search to perform ('vector', 'keyword', or 'hybrid'). Defaults to the class-level default search type.
            **kwargs: Additional arguments for specific search types (e.g., weights for hybrid search).

        Returns:
            List[Tuple[Document, float]]: A list of tuples containing Documents and their similarity scores.
        """
        search_type = search_type or self.default_search_type

        if search_type == "vector":
            return self._run_vector_search(query, k)
        elif search_type == "keyword":
            return self._run_keyword_search(query, k)
        elif search_type == "hybrid":
            return self._run_hybrid_search(query, k, **kwargs)
        else:
            raise ValueError(
                "Invalid search type. Choose 'vector', 'keyword', or 'hybrid'."
            )

    def _run_vector_search(self, query: str, k: int) -> List[Tuple[Document, float]]:
        """
        Run the vector-based similarity search and return results with scores.

        Args:
            query (str): The search query.
            k (int): Number of top results to return.

        Returns:
            List[Tuple[Document, float]]: A list of Documents and their similarity scores.
        """
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np

        query_embedding = self._embedding_function.embed_query(query)
        query_embedding = np.array(query_embedding).reshape(1, -1)

        # Cypher query to retrieve nodes and their embeddings from Memgraph
        cypher_query = """
        MATCH (n:Chunk)
        WHERE n.embedding IS NOT NULL
        RETURN n.text_data AS text_data, n.embedding AS embedding, n
        LIMIT 1000
        """
        with self.driver.session() as session:
            results = session.run(cypher_query)
            embeddings = []
            docs = []
            for record in results:
                doc_embedding = np.array(record["embedding"], dtype="float32")
                if doc_embedding.ndim == 1:
                    doc_embedding = doc_embedding.reshape(1, -1)
                embeddings.append(doc_embedding)
                docs.append(record)

        if len(embeddings) == 0:
            raise ValueError("No embeddings found in the database.")

        # Stack all embeddings and calculate cosine similarity
        embeddings = np.vstack(embeddings)
        similarities = cosine_similarity(query_embedding, embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:k]

        # Prepare the results as a list of (Document, similarity_score)
        docs_and_scores = []
        for i in top_indices:
            doc_text = docs[i]["text_data"]
            metadata = dict(docs[i]["n"].items())
            document = Document(page_content=doc_text, metadata=metadata)
            docs_and_scores.append((document, similarities[i]))

        return docs_and_scores

    def _run_keyword_search(self, query: str, k: int) -> List[Tuple[Document, float]]:
        """
        Run the keyword-based search and return results.

        Args:
            query (str): The search query.
            k (int): Number of top results to return.

        Returns:
            List[Tuple[Document, float]]: A list of Documents and their similarity scores (set to 1.0 for keyword matches).
        """
        cypher_query = """
        MATCH (n:Chunk)
        WHERE n.text_data CONTAINS $query
        RETURN n.text_data AS text_data, n
        LIMIT $limit
        """
        with self.driver.session() as session:
            results = session.run(cypher_query, parameters={"query": query, "limit": k})
            docs_and_scores = []
            for record in results:
                doc_text = record["text_data"]
                metadata = dict(record["n"].items())
                document = Document(page_content=doc_text, metadata=metadata)
                docs_and_scores.append(
                    (document, 1.0)
                )  # Keyword match score is set to 1
        return docs_and_scores

    def _run_hybrid_search(
        self,
        query: str,
        k: int,
        keyword_weight: float = 0.5,
        vector_weight: float = 0.5,
    ) -> List[Tuple[Document, float]]:
        """
        Run the hybrid search combining keyword and vector search.

        Args:
            query (str): The search query.
            k (int): Number of top results to return.
            keyword_weight (float): Weight to give to keyword search results.
            vector_weight (float): Weight to give to vector search results.

        Returns:
            List[Tuple[Document, float]]: A list of Documents and their combined similarity scores.
        """
        total_weight = keyword_weight + vector_weight
        keyword_weight /= total_weight
        vector_weight /= total_weight

        keyword_results = self._run_keyword_search(query, k)
        vector_results = self._run_vector_search(query, k)

        combined_results = {}

        # Combine keyword and vector results with their respective weights
        for document, score in keyword_results:
            doc_text = document.page_content
            if doc_text not in combined_results:
                combined_results[doc_text] = {
                    "document": document,
                    "score": score * keyword_weight,
                }
            else:
                combined_results[doc_text]["score"] += score * keyword_weight

        for document, similarity_score in vector_results:
            doc_text = document.page_content
            if doc_text not in combined_results:
                combined_results[doc_text] = {
                    "document": document,
                    "score": similarity_score * vector_weight,
                }
            else:
                combined_results[doc_text]["score"] += similarity_score * vector_weight

        sorted_results = sorted(
            combined_results.values(), key=lambda x: x["score"], reverse=True
        )
        return [(result["document"], result["score"]) for result in sorted_results[:k]]

    def search(
        self, query: str, search_type: Optional[str] = None, k: int = 4, **kwargs
    ) -> List[Document]:
        """
        Search function to handle different search types (vector, keyword, or hybrid).

        Args:
            query (str): The search query.
            search_type (Optional[str]): The type of search to perform ('vector', 'keyword', or 'hybrid'). Defaults to the class-level default search type.
            k (int): Number of results to return. Defaults to 4.
            **kwargs: Additional arguments for specific search types (e.g., weights for hybrid search).

        Returns:
            List[Document]: List of documents based on the chosen search method.
        """
        return [
            doc
            for doc, _ in self._similarity_search_with_score(
                query, k=k, search_type=search_type, **kwargs
            )
        ]

    def retrieve(
        self, query: str, top_k: int = 5, search_type: Optional[str] = None, **kwargs
    ) -> Tuple[List[str], List[float]]:
        """
        Retrieve relevant documents and their scores for a given query, supporting different search types.

        Args:
            query (str): The search query.
            top_k (int): Number of top results to return. Defaults to 5.
            search_type (Optional[str]): The type of search to perform ('vector', 'keyword', or 'hybrid'). Defaults to the class-level default search type.
            **kwargs: Additional arguments for specific search types (e.g., weights for hybrid search).

        Returns:
            Tuple[List[str], List[float]]: A tuple containing a list of document contents and their respective scores.
        """
        docs_and_scores = self._similarity_search_with_score(
            query, k=top_k, search_type=search_type, **kwargs
        )
        context = [doc.page_content for doc, _ in docs_and_scores]
        scores = [score for _, score in docs_and_scores]
        return context, scores
