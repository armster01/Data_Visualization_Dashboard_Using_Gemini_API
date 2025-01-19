import streamlit as st
from typing import Callable, Any
from functools import wraps

class ChatError(Exception):
    """Custom exception for chat-related errors"""
    pass

def handle_errors(func: Callable) -> Callable:
    """Decorator for handling errors in the application"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            if isinstance(e, ChatError):
                st.warning("Please try rephrasing your question.")
            else:
                st.error("Please check your API key and try again.")
            return None
    return wrapper