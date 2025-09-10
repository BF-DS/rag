# Use official Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /rag

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files (but not .env for security)
# local folder destination
COPY streamlit-rag/ ./streamlit-rag 
# copy the history_aware_rag.py wit the chatbot 
COPY history_aware_rag.py ./streamlit-rag/

# Expose Streamlit default port
EXPOSE 8501

# Set working directory inside the app folder
WORKDIR /rag/streamlit-rag

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
# Note: The vector store is not copied into the Docker image to keep the image size small. 
# Instead, you need to mount the vector store directory as a volume when running the container.