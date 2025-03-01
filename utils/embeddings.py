"""
Utility functions for handling document embeddings and FAISS database operations.
"""
from typing import List
import os
import shutil
from pathlib import Path
import faiss
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from loguru import logger

class DocumentEmbedder:
    """Handles document embedding and FAISS database operations."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        model_name: str = "all-MiniLM-L6-v2"
    ):
        """
        Initialize the document embedder.
        
        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            model_name: HuggingFace model name for embeddings
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'}
        )

        logger.info(f"The model being used to create embeddings is {model_name}.")
        logger.info("The device being used to create embeddings is cpu.")       

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def process_pdf(self, pdf_path: str) -> List[str]:
        """
        Process a single PDF file into chunks.
        pdf_path: Path to the PDF file   
        Returns: List of text chunks
        """
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        return self.text_splitter.split_documents(pages)

    def create_faiss_db(self, folder_path: str, db_path: str) -> None:
        """
        Create a FAISS database from PDFs in a folder.
        param folder_path: Path to folder containing PDFs
        param db_path: Path where FAISS database will be stored
        """
        # Remove existing database if it exists
        if os.path.exists(db_path):
            shutil.rmtree(db_path)
            logger.info(f"Removed existing database at {db_path}")

        all_chunks = []
        pdf_files = Path(folder_path).glob("*.pdf")

        for pdf_file in pdf_files:
            try:
                chunks = self.process_pdf(str(pdf_file))
                all_chunks.extend(chunks)
                logger.info(f"Processed {pdf_file}")
            except Exception as e:
                logger.error(f"Error processing {pdf_file}: {str(e)}")

        if not all_chunks:
            logger.error("No valid chunks were generated from the PDFs")
            raise ValueError("No valid chunks were generated from the PDFs")

        # Create directory if it doesn't exist   
        log_dir = Path("database/faiss_db")
        log_dir.mkdir(exist_ok=True, parents=True)

        # Create embeddings using the correct method
        texts = [chunk.page_content for chunk in all_chunks]
        embeddings = self.embeddings.embed_documents(texts)
        embeddings_array = np.array(embeddings, dtype=np.float32)

        # Initialize FAISS index
        dimension = len(embeddings[0])
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings_array)  
        faiss.write_index(index, str(Path(db_path) / "index.faiss"))

        # Save the documents for later retrieval
        np.save(str(Path(db_path) / "documents.npy"), all_chunks)
        logger.info(f"Created FAISS database at {db_path}")
