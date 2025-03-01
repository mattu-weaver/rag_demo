"""
Document upload page implementation
"""
from pathlib import Path
import streamlit as st
from loguru import logger
from utils import count_pdf_files, path_exists
from utils.embeddings import DocumentEmbedder
from .base_page import StreamlitPage
from typing import Dict

class UploadPage(StreamlitPage):
    """
    Home page for this streamlit application, derives from StreamlitPage.
    """

    @property
    def page_name(self) -> str:
        """
        Implementation of page_name from the page base class: StreamlitPage.
        Returns: The name of this page.
        """
        return "Upload Documents"

    def render_page(self, cfg_: Dict[str, any]) -> None:
        """
        Base class implementation to render this page.
        """
        # Add sidebar controls
        with st.sidebar:
            st.header("Model Parameters")
            model_name = st.text_input(
                "Embedding Model",
                value="all-MiniLM-L6-v2",
                help="The model to use for embeddings."
            )
            
            st.header("Chunking Parameters")
            chunk_size = st.slider(
                "Chunk Size",
                min_value=100,
                max_value=2000,
                value=500,
                step=20,
                help="Number of characters in each text chunk"
            )
            chunk_overlap = st.slider(
                "Chunk Overlap",
                min_value=0,
                max_value=500,
                value=150,
                step=10,
                help="Number of characters to overlap between chunks"
            )

            show_samples = st.checkbox(
                "Show Sample Chunks",
                value=False,
                help="Display 2 random sample chunks after processing"
            )

        st.title("PDF Folder Analyzer")

        # Textbox for folder path input
        text_default = cfg_['coding_defaults']['pdf_folder']
        folder_path = st.text_input("Enter the path to a local folder:", value=text_default)

        # Add button to run tests
        if st.button("Process Files"):
            with st.spinner("Processing PDFs and creating embeddings..."):
                if folder_path:
                    if not path_exists(folder_path):
                        message = (
                            "The process files button was clicked but the specified folder does not exist. "
                            f"[{folder_path}]"
                        )
                        st.error("The folder you specified does not exist.")
                        logger.warning(message)
                    else:
                        try:
                            # Count PDF files in the folder
                            pdf_count = count_pdf_files(folder_path)
                            if pdf_count == 0:
                                st.warning("No PDF files found in the specified folder.")
                                return

                            st.info(f"Found {pdf_count} PDF file(s) in the folder.")
                            
                            # Create embeddings and FAISS database
                            embedder = DocumentEmbedder(
                                chunk_size=chunk_size,
                                chunk_overlap=chunk_overlap,
                                model_name=model_name
                            )
                            
                            # Process first PDF to show samples if requested
                            if show_samples:
                                first_pdf = next(Path(folder_path).glob("*.pdf"))
                                chunks = embedder.process_pdf(str(first_pdf))
                                if len(chunks) >= 2:
                                    st.subheader("Sample Chunks")
                                    st.info(f"From file: {first_pdf.name}")
                                    for i, chunk in enumerate(chunks[:2], 1):
                                        with st.expander(f"Chunk {i}"):
                                            st.text(chunk.page_content)
                            
                            embedder.create_faiss_db(folder_path, "database/faiss_db")
                            
                            st.success("Successfully created FAISS database!")
                        except Exception as e:
                            st.error(f"Error processing documents: {str(e)}")
                            logger.error(f"Error during document processing: {str(e)}")
                else:
                    st.warning("Please enter a folder path.")
                    logger.warning("The Process Files button was clicked but no folder path was provided.")

