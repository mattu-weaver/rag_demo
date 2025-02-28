"""
Document upload page implementation
"""
import streamlit as st
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
        st.title("Upload Documents")
        uploaded_files = st.file_uploader(
            "Upload your documents",
            type=["pdf", "txt", "docx"],
            accept_multiple_files=True
        )
        st.write("Upload your documents for processing")
