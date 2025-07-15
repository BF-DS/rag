# History-Aware RAG Chatbot using LangChain and ChromaDB

import os
from dotenv import load_dotenv
from typing import List, Tuple, Dict, Any

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

class HistoryAwareRAGChatbot:
    def __init__(self, vector_store_path: str = "./vector_store", collection_name: str = "book-rag"):
        """
        Initialize the History-Aware RAG Chatbot.
        
        Args:
            vector_store_path (str): Path to the ChromaDB vector store
            collection_name (str): Name of the ChromaDB collection
        """
        # Load environment variables
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=self.openai_api_key
        )
        
        # Initialize vector store
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=vector_store_path
        )
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            openai_api_key=self.openai_api_key
        )
        
        # Create retriever
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        
        # Setup history-aware retriever and QA chain
        self._setup_chains()
    
    def _setup_chains(self):
        """Setup the history-aware retriever and QA chains."""
        
        # Contextualize question prompt
        contextualize_q_system_prompt = """Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is."""
        
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        # Create history-aware retriever
        self.history_aware_retriever = create_history_aware_retriever(
            self.llm, self.retriever, contextualize_q_prompt
        )
        
        # QA system prompt
        qa_system_prompt = """You are an assistant for question-answering tasks. \
        Use the following pieces of retrieved context to answer the question. \
        If you don't know the answer, just say that you don't know. \
        Use three sentences maximum and keep the answer concise.
        
        Context:
        {context}"""
        
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        # Create QA chain
        question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        
        # Create full RAG chain
        self.rag_chain = create_retrieval_chain(
            self.history_aware_retriever, question_answer_chain
        )
    
    def query(self, question: str, chat_history: List[Tuple[str, str]] = None) -> Dict[str, Any]:
        """
        Query the RAG system with conversation history.
        
        Args:
            question (str): The user's question
            chat_history (List[Tuple[str, str]]): List of (human_message, ai_message) tuples
            
        Returns:
            Dict[str, Any]: Response containing answer and source documents
        """
        if chat_history is None:
            chat_history = []
        
        # Convert chat history to LangChain message format
        history_langchain_format = []
        for human, ai in chat_history:
            history_langchain_format.append(HumanMessage(content=human))
            history_langchain_format.append(AIMessage(content=ai))
        
        # Invoke the RAG chain
        response = self.rag_chain.invoke({
            "input": question,
            "chat_history": history_langchain_format
        })
        
        return {
            "answer": response["answer"],
            "source_documents": response.get("context", []),
            "question": question
        }
    
    def get_similar_documents(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Get similar documents for a query.
        
        Args:
            query (str): The search query
            k (int): Number of documents to return
            
        Returns:
            List[Dict[str, Any]]: List of similar documents with metadata
        """
        docs = self.vector_store.similarity_search_with_score(query, k=k)
        
        result = []
        for doc, score in docs:
            result.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "similarity_score": score
            })
        
        return result
    
    def clear_history(self):
        """Clear the chat history (for Streamlit session state)."""
        pass  # This will be handled by Streamlit session state

# Convenience function for backward compatibility
def query(question: str, chat_history: List[Tuple[str, str]] = None) -> Dict[str, Any]:
    """
    Convenience function to query the RAG system.
    Creates a new chatbot instance each time (not efficient for production).
    """
    chatbot = HistoryAwareRAGChatbot()
    return chatbot.query(question, chat_history)

if __name__ == "__main__":
    # Test the chatbot
    chatbot = HistoryAwareRAGChatbot()
    
    # Test basic query
    response = chatbot.query("What are large language models?")
    print("Answer:", response["answer"])
    print("\nSource documents:", len(response["source_documents"]))
    
    # Test with history
    chat_history = [("What are large language models?", response["answer"])]
    follow_up = chatbot.query("How do they work?", chat_history)
    print("\nFollow-up Answer:", follow_up["answer"])
