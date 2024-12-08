import streamlit as st
import json

class ChatInterface:
    def __init__(self, agent):
        self.agent = agent
        if 'messages' not in st.session_state:
            st.session_state.messages = []

    def display(self):
        st.header("Chat with our Food Ordering Assistant")

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("What would you like to order?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get assistant response
            with st.chat_message("assistant"):
                response = self.agent.process_message(
                    prompt,
                    st.session_state.messages
                )
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})