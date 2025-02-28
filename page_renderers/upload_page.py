"""
Document upload page implementation
"""

import os
import streamlit as st
from loguru import logger
from utils import count_pdf_files, path_exists
from .base_page import StreamlitPage


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

    def render_page(self) -> None:
        """
        Base class implementation to render this page.
        """
        st.title("PDF Folder Analyzer")

        # Textbox for folder path input
        folder_path = st.text_input("Enter the path to a local folder:")

        # Add button to run tests
        if st.button("Process Files"):
            with st.spinner("Running tests..."):
                if folder_path:
                    if not path_exists(folder_path):
                        message = (
                            "The process files button was clicked but the specified folder does not exist. "
                            f"[{folder_path}]"
                        )
                        st.error("The folder you specified does not exist.")
                        logger.warning(message)
                    else:
                        # Count PDF files in the folder
                        pdf_count = count_pdf_files(folder_path)
                        st.success(f"Found {pdf_count} PDF file(s) in the folder.")
                else:
                    st.warning("Please enter a folder path.")
                    logger.warning("The Process Files button was clicked but no folder path was provided.")

