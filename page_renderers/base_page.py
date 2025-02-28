"""
Base abstract class for Streamlit pages
"""
from abc import ABC, abstractmethod


class StreamlitPage(ABC):
    """Abstract base class that all Streamlit pages must inherit from."""

    @property
    @abstractmethod
    def page_name(self) -> str:
        """
        Returns the name of the page as it should appear in navigation.
        
        Returns:
            str: The page name
        """


    @abstractmethod
    def render_page(self) -> None:
        """
        Renders the page content in Streamlit.
        This method must be implemented by all page classes.
        """
