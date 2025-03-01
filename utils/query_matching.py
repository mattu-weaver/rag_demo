"""
Utility functions for matching queries against the FAISS database.
"""
from typing import List, Tuple
from pathlib import Path
import numpy as np
import faiss
from langchain_huggingface import HuggingFaceEmbeddings
from loguru import logger


class QueryMatcher:
    """Handles matching queries against the FAISS database."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        k: int = 5
    ):
        """
        Initialize the query matcher.
        
        Args:
            model_name: HuggingFace model name for embeddings
            k: Number of matches to return
        """
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'}
        )
        self.k = k

    def match_query(self, query: str, db_path: str) -> List[Tuple[str, float]]:
        """
        Match a query against the FAISS database.
        
        Args:
            query: The query string
            db_path: Path to the FAISS database directory
            
        Returns:
            List of tuples containing (chunk_text, similarity_score)
        """
        try:
            # Load the FAISS index
            index_path = Path(db_path) / "index.faiss"
            if not index_path.exists():
                raise FileNotFoundError(f"FAISS index not found at {index_path}")
                
            index = faiss.read_index(str(index_path))
            
            # Load the stored documents
            docs_path = Path(db_path) / "documents.npy"
            if not docs_path.exists():
                raise FileNotFoundError(f"Document store not found at {docs_path}")
                
            stored_docs = np.load(str(docs_path), allow_pickle=True)
            
            # Generate embedding for the query
            query_embedding = self.embeddings.embed_query(query)
            query_embedding = np.array([query_embedding], dtype=np.float32)
            
            # Search the index
            distances, indices = index.search(query_embedding, self.k)
            
            # Get matching chunks with their scores
            results = []
            for idx, dist in zip(indices[0], distances[0]):
                if idx < len(stored_docs):  # Ensure index is valid
                    similarity = 1 - dist  # Convert distance to similarity score
                    results.append((stored_docs[idx].page_content, similarity))
            
            return results
            
        except Exception as e:
            logger.error(f"Error matching query: {str(e)}")
            raise RuntimeError(f"Failed to match query: {str(e)}")
