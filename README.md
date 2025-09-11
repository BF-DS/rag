# Conversational RAG

This project implements a Retrieval-Augmented Generation (RAG) pipeline using Python. RAG combines information retrieval with generative models to answer queries based on both external documents and language model capabilities. 
## Tools & Technologies

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-4B8BBE?logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)
![Chroma](https://img.shields.io/badge/Chroma-FF6F00?logo=chroma&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)

# Table of Contents
- [Process Overview](#process-overview)
  - [Vector store loading](#vector-store-loading)
  - [Retrieval](#retrieval)
- [External Document](#external-document)
- [Project Structure](#project-structure)
- [Installation and Usage](#installation-and-usage)
- [Running the App](#running-the-app)
- [Debugging](#debugging)


## Process Overview
### Vector store loading
- **Document Ingestion**: Load documents from a specified directory.
- **Document Splitting**: Split documents into manageable chunks.
- **Vectorization**: Convert document chunks into vector embeddings using OpenAI embeddings `text-embedding-3-small`. Embeddings are numerical representation of text that capture semantic meaning. 
- **Storage**: Store the vectorized chunks in a vector store (Chroma) for efficient retrieval.

<p align="left">
    <img src="img/vector-store-loading.jpg" alt="retrieval-pipeline" width="600"/>
</p> 

*Source: DeepLearning.AI*

### retrieval
- **Retrieval**: Use a vector store to retrieve relevant chunks based on a query. Integration with a large language model `gpt-4o-mini` for generating answers.
- **Answer Generation**: Generate answers using the retrieved chunks and the language model.
- **Contextual Awareness**: Maintain conversation history to provide context for follow-up questions.
- **Source Document Display**: Show the source documents used to generate the answer.

<p align="left">
    <img src="img/retrieval.jpg" alt="retrieval-pipeline" width="600"/>
</p> 

*Source: DeepLearning.AI*

## External Document
As external document it uses the book 'Praxiseinstieg Large Language Models' by Sinan Ozdemir (German edition).

<p align="center">
    <img src="img/Praxiseinstieg-LLM.jpg" alt="Praxiseinstieg Large Language Models" width="300"/>
</p>

## Project Structure

- `README.md`: This file, providing an overview of the project.
- `streamlit-rag/`: Contains the Streamlit app for the RAG process.
- `history_aware_rag.py`: Implements the RAG pipeline with history-aware retrieval.
- `src/`: Contains utility functions for document loading, splitting, and vectorization.
- `basics/`: Jupyter notebooks demonstrating concepts for the RAG process.
- `requirements.txt`: Lists the required Python packages for the project.
- `vector_store/`: Contains the vector store implementation using Chroma.

# Installation and Usage
Create a .env file in the root directory with the following content:
```plaintext
OPENAI_API_KEY=your_openai_api_key
```
Note: Make sure to not use quotes around the API key. Otherwise it will be treated as a string literal and may not work as expected.
## Docker
Build the Docker image using the following command:
```bash
docker build -t streamlit-rag .
```
The -t flag allows you to tag the image with a name (in this case, `streamlit-rag`), making it easier to reference later.

Run the Docker container with the following command:
```bash
docker run -p 8501:8501 --env-file .env -v "$(pwd)/vector_store:/rag/vector_store" streamlit-rag
```
**Explanation of the command:**
8501 is the default port for Streamlit apps, and it is mapped to the same port on the host machine. The `--env-file .env` option allows you to pass environment variables from the `.env` file to the container. It´s not copied into the image for security reasons. 
The vector store is not copied into the Docker image to keep the image size small. And also to allow for easy updates to the vector store without needing to rebuild the entire Docker image. Instead, you need to mount the vector store directory as a volume when running the container. You can do this by adding the `-v` option to the `docker run` command with the path to the vector store directory on your host machine and the path where you want to mount it inside the container (`/rag/vector_store` in this case). Replace `$(pwd)/vector_store` with the actual path to your vector store directory if you are not running the command from the root directory of the project. `streamlit-rag` is the name of the Docker image to run.

# Running the App
After running the command above, the terminal should display a message indicating that the app is running on `http://localhost:8501` or `http://0.0.0.0:8501`. You can open this URL in your web browser to access the app. You can now enter your questions in the input field and the LLM will answer them based on the ingested documents. The app also displays the source documents used to generate the answer, allowing you to verify the information provided by the LLM.

![rag-chat](img/rag_chat.gif)

Follow up questions are also supported, allowing you to ask further questions based on the previous answers. The app will maintain the context of the conversation and provide relevant answers based on the ingested documents.

![history-aware-rag-chat](img/history-aware_rag_chat.gif)


If the LLM does not have enough context to answer a question, it will inform you about it. You can then provide additional context or ask a different question.

![out-of-context-rag-chat](img/outofcontext_rag_chat.gif)

# Debugging
## Conda Env
When not using a container it´s recommended to use a virtual environment to manage dependencies. You can use `anaconda` for this purpose. The following commands will create a new conda environment and install the required packages:   
```bash
conda create -n rag-env python=3.12
conda activate rag-env
pip install -r requirements.txt
```
After creating the environment and installing the dependencies, you can run the streamlit app with the following command:
```bash
cd streamlit-rag
streamlit run app.py
```
It´s important to run the app from within the `streamlit-rag` directory, as the app relies on relative paths to access other modules and resources.