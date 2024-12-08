import streamlit as st
from dotenv import load_dotenv
import sys
import os

load_dotenv()

# Add parent directory to path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import Database
from backend.rag import RAGSystem
from backend.agent import OrderAgent
from components.chat import ChatInterface
from components.menu import MenuDisplay

def main():
    st.set_page_config(
        page_title="Restaurant Chatbot",
        page_icon="🍽️",
        layout="wide"
    )

    # Initialize components
    if 'database' not in st.session_state:
        st.session_state.database = Database()
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = RAGSystem()
    if 'agent' not in st.session_state:
        st.session_state.agent = OrderAgent(
            st.session_state.database,
            st.session_state.rag_system
        )

    # Page layout
    st.title("🍽️ Restaurant Chatbot")
    
    # Two-column layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Chat interface
        chat_interface = ChatInterface(st.session_state.agent)
        chat_interface.display()
    
    with col2:
        # Menu display
        menu_display = MenuDisplay(st.session_state.database)
        menu_display.show()

if __name__ == "__main__":
    main()