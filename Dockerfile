# Use official Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files (but not .env for security)
# local folder destination
COPY streamlit-rag/ ./streamlit-rag 
# copy the history_aware_rag.py
COPY history_aware_rag.py ./streamlit-rag/

# Expose Streamlit default port
EXPOSE 8501

# Set working directory inside the app folder
WORKDIR /app/streamlit-rag

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
