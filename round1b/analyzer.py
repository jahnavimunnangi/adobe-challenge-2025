import os
import json
import fitz  # PyMuPDF
import re
import datetime
from sentence_transformers import SentenceTransformer, util

# Load persona and job-to-be-done from a text file
def load_persona(persona_path):
    with open(persona_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    persona = lines[0].replace("Persona:", "").strip()
    job = lines[1].replace("Task:", "").strip()
    return persona, job

# Extract paragraphs from each PDF page
def extract_text_chunks(pdf_path):
    doc = fitz.open(pdf_path)
    chunks = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        for para in text.split("\n\n"):
            para_clean = para.strip().replace("\n", " ")
            if len(para_clean.split()) > 5:  # Filter out short lines
                chunks.append({
                    "text": para_clean,
                    "page": page_num,
                    "doc": os.path.basename(pdf_path)
                })
    return chunks

# Analyze documents for relevance to the given persona and task
def analyze_documents(input_dir, persona_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    persona, task = load_persona(persona_path)
    print(f"\nPersona: {persona}\nTask: {task}")

    prompt = f"{persona} needs to: {task}"

    # Load sentence embedding model
    model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")

    all_chunks = []
    docs = []

    # Extract text from all PDFs in input folder
    for file in os.listdir(input_dir):
        if file.lower().endswith(".pdf"):
            path = os.path.join(input_dir, file)
            docs.append(file)
            chunks = extract_text_chunks(path)
            all_chunks.extend(chunks)

    print(f"\nTotal extracted text chunks: {len(all_chunks)}")

    # Embed and rank all chunks by similarity to the task
    query_embedding = model.encode(prompt, convert_to_tensor=True)
    chunk_texts = [chunk["text"] for chunk in all_chunks]
    chunk_embeddings = model.encode(chunk_texts, convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(query_embedding, chunk_embeddings)[0]
    ranked = sorted(zip(similarities, all_chunks), key=lambda x: x[0], reverse=True)

    # Select top N most relevant chunks
    top_n = min(10, len(ranked))
    results = []
    for rank, (score, chunk) in enumerate(ranked[:top_n], start=1):
        results.append({
            "document": chunk["doc"],
            "page": chunk["page"],
            "section_title": chunk["text"][:60] + "...",
            "importance_rank": rank,
            "subsections": [
                {
                    "page": chunk["page"],
                    "text": chunk["text"]
                }
            ]
        })

    # Final output JSON
    output = {
        "metadata": {
            "documents": docs,
            "persona": persona,
            "job_to_be_done": task,
            "timestamp": datetime.datetime.now().isoformat()
        },
        "results": results
    }

    with open(os.path.join(output_dir, "result.json"), "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("Done. Output saved to output/result.json")

if __name__ == "__main__":
    analyze_documents("input", "persona.txt", "output")
