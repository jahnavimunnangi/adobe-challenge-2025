FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install pymupdf

CMD ["python", "extractor.py"]
