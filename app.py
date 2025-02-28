"""
The application entry point with multi-page Streamlit interface.
"""

from typing import Dict, Type
import streamlit as st
from loguru import logger
from app_config import AppConfig, ConfigLoader, LoggerConfigurator
from page_renderers import StreamlitPage, HomePage, UploadPage, QueryPage


class PageManager:
    """Manages the available pages and their display."""

    def __init__(self, page_dict: Dict[str, Type[StreamlitPage]]):
        self.pages = page_dict

    def set_global_sidebar_widgets(self) -> str:
        """Displays page navigation in the sidebar."""
        st.sidebar.title("Navigation")
        selected_page = st.sidebar.selectbox("Select a page", list(self.pages.keys()))
        return selected_page

    def display_page(self, page_name: str) -> None:
        """Displays the selected page."""
        logger.info(f"Displaying page: {page_name}")
        page_instance = self.pages[page_name]()
        page_instance.render_page()


def get_pages() -> Dict[str, Type[StreamlitPage]]:
    """Get the mapping of page names to their class implementations."""
    pages = [HomePage, UploadPage, QueryPage]
    return {page_class().page_name: page_class for page_class in pages}


def setup_streamlit_interface() -> None:
    """Sets up the basic Streamlit interface."""
    st.set_page_config(page_title="RAG Document System", page_icon="📚", layout="wide")


def main(app_cfg: AppConfig, page_mgr: PageManager) -> None:
    """
    Main application entry point.

    Args:
        app_config: The application configuration object.
        page_manager: The object to manage the pages.
    """
    logger = app_cfg.setup_logging()
    setup_streamlit_interface()
    # Sidebar navigation
    selected_page = page_mgr.set_global_sidebar_widgets()
    st.session_state.current_page = selected_page

    # Display selected page
    page_mgr.display_page(selected_page)


if __name__ == "__main__":
    # Dependency Injection in action!
    config_loader = ConfigLoader(".streamlit/config.toml")
    logger_configurator = LoggerConfigurator()
    app_config = AppConfig(config_loader, logger_configurator)
    page_dictionary = get_pages()
    page_manager = PageManager(page_dictionary)

    main(app_config, page_manager)




