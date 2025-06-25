# BGB Chatbot

import streamlit as st

# Center the image using Streamlit's columns
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("img/Praxiseinstieg-LLM.jpg")

st.subheader("Please enter your Query")

# initialize chat messages from histroy on app rerun
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_history = []

# Accept user input
if prompt := st.chat_input("Ask a question about the Book"):
    # Invoke the function with the Retriever with chat histroy and display responses in chat container in query
    with st.spinner("Generating response..."):
        response = query(question=prompt, chat_history=st.session_state.chat_history)
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            st.markdown(response["answer"])

        # Append user message to chat histroy
        st.seassion_state.messages.append({"role": "user", "content": prompt})
        # Append assistant message to chat histroy
        st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
        st.session_state.chat_history.append((prompt, response["answer"]))  