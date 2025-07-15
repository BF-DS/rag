import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from history_aware_rag import HistoryAwareRAGChatbot

st.set_page_config(page_title="History-Aware RAG Chatbot", page_icon="🤖", layout="centered")
st.title("History-Aware RAG Chatbot")

# Initialize chatbot in session state
def get_chatbot():
    if "chatbot" not in st.session_state:
        st.session_state["chatbot"] = HistoryAwareRAGChatbot()
    return st.session_state["chatbot"]

# Initialize chat history in session state
def get_history():
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    return st.session_state["chat_history"]

chatbot = get_chatbot()
chat_history = get_history()

st.markdown("""
This app lets you chat with a RAG-powered assistant using a persistent ChromaDB vector store. Your conversation history is used to improve retrieval and answers.
""")

# Chat interface
with st.form("chat_form"):
    user_input = st.text_input("Your message:", "", key="user_input")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    # Query chatbot
    response = chatbot.query(user_input, chat_history)
    # Update history
    chat_history.append((user_input, response["answer"]))
    st.session_state["chat_history"] = chat_history

# Display chat history
if chat_history:
    st.subheader("Conversation History")
    for i, (human, ai) in enumerate(chat_history):
        st.markdown(f"**You:** {human}")
        st.markdown(f"**Bot:** {ai}")

# Option to clear history
if st.button("Clear Conversation"):
    st.session_state["chat_history"] = []
    st.rerun()

# Show source documents for last answer
if chat_history:
    last_question = chat_history[-1][0]
    last_response = chatbot.query(last_question, chat_history[:-1])
    source_docs = last_response.get("source_documents", [])
    if source_docs:
        st.subheader("Source Documents")
        for i, doc in enumerate(source_docs):
            st.markdown(f"**Document {i+1}:**")
            # Use attribute access for Pydantic objects
            st.code(getattr(doc, "page_content", getattr(doc, "content", "")))
            metadata = getattr(doc, "metadata", None)
            if metadata:
                # Only show selected fields from metadata
                fields = ["page_label", "title", "subject", "author"]
                filtered = {k: metadata.get(k) for k in fields if k in metadata}
                if filtered:
                    meta_str = ", ".join(f"{k}: {v}" for k, v in filtered.items() if v)
                    st.caption(meta_str)
