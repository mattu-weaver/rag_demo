"""
Query page implementation
"""
import streamlit as st
from .base_page import StreamlitPage
from typing import Dict

class QueryPage(StreamlitPage):
    """
    Query page for this streamlit application, derives from StreamlitPage.
    """

    @property
    def page_name(self) -> str:
        """
        Implementation of page_name from the page base class: StreamlitPage.
        Returns: The name of this page.
        """        
        return "Query Documents"

    def render_page(self, cfg_: Dict[str, any]) -> None:
        st.title("Query Documents")
        query = st.text_input("Enter your question:")
        st.write("Ask questions about your documents")
