FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files into container
COPY . .

# Install required packages
RUN pip install --no-cache-dir pymupdf sentence-transformers torch

# Pre-download the model (offline execution)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-MiniLM-L6-v2')"

# Entry point
CMD ["python", "analyzer.py"]
