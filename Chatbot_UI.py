# History-Aware RAG Chatbot UI

import streamlit as st
import time
from history_aware_rag import HistoryAwareRAGChatbot

# Page configuration
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize the chatbot (cached for performance)
@st.cache_resource
def get_chatbot():
    """Initialize and cache the RAG chatbot."""
    try:
        return HistoryAwareRAGChatbot()
    except Exception as e:
        st.error(f"Error initializing chatbot: {e}")
        st.info("Please make sure your .env file contains a valid OPENAI_API_KEY")
        return None

# Sidebar
with st.sidebar:
    st.title("🤖 RAG Chatbot")
    st.markdown("---")
    
    # Model information
    st.subheader("Model Info")
    st.write("🧠 **LLM:** GPT-4o-mini")
    st.write("🔍 **Embeddings:** text-embedding-3-small")
    st.write("💾 **Vector Store:** ChromaDB")
    
    st.markdown("---")
    
    # Chat controls
    st.subheader("Chat Controls")
    if st.button("🗑️ Clear Chat History", help="Clear all chat messages"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()
    
    # Show statistics
    if "messages" in st.session_state:
        st.metric("Messages", len(st.session_state.messages))
        st.metric("Conversations", len(st.session_state.chat_history))

# Main content
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("img/Praxiseinstieg-LLM.jpg", caption="Large Language Models Praxiseinstieg")

st.title("📚 History-Aware RAG Chatbot")
st.subheader("Stellen Sie Ihre Fragen zum Buch - der Chatbot berücksichtigt den Gesprächsverlauf!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_history = []

# Initialize chatbot
chatbot = get_chatbot()

if chatbot is None:
    st.stop()

# Display chat messages from history on app rerun
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show source documents for assistant messages
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📄 Quelldokumente anzeigen"):
                    for i, source in enumerate(message["sources"], 1):
                        st.write(f"**Quelle {i}:**")
                        st.write(f"*Seite:* {source.get('page', 'N/A')}")
                        st.write(f"*Ähnlichkeit:* {source.get('similarity_score', 'N/A'):.3f}")
                        st.write(f"*Inhalt:* {source.get('content', '')[:200]}...")
                        st.markdown("---")

# Chat input
if prompt := st.chat_input("Geben Sie Ihre Frage ein..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)
    
    # Generate response
    with chat_container:
        with st.chat_message("assistant"):
            with st.spinner("Wird verarbeitet..."):
                try:
                    # Get response from RAG system
                    response = chatbot.query(
                        question=prompt, 
                        chat_history=st.session_state.chat_history
                    )
                    
                    # Display the answer
                    st.markdown(response["answer"])
                    
                    # Prepare source information
                    sources = []
                    if response.get("source_documents"):
                        for doc in response["source_documents"]:
                            sources.append({
                                "content": doc.page_content,
                                "page": doc.metadata.get("page", "N/A"),
                                "source": doc.metadata.get("source", "N/A")
                            })
                    
                    # Show source documents
                    if sources:
                        with st.expander("📄 Quelldokumente anzeigen"):
                            for i, source in enumerate(sources, 1):
                                st.write(f"**Quelle {i}:**")
                                st.write(f"*Seite:* {source.get('page', 'N/A')}")
                                st.write(f"*Inhalt:* {source.get('content', '')[:200]}...")
                                st.markdown("---")
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response["answer"],
                        "sources": sources
                    })
                    
                    # Update chat history for context
                    st.session_state.chat_history.append((prompt, response["answer"]))
                    
                except Exception as e:
                    st.error(f"Fehler bei der Verarbeitung: {e}")
                    st.info("Bitte überprüfen Sie Ihre Konfiguration und versuchen Sie es erneut.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    🤖 Powered by LangChain, OpenAI, and ChromaDB | 
    📚 History-Aware RAG System
    </div>
    """, 
    unsafe_allow_html=True
)  