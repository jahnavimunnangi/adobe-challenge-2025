# Adobe Challenge - Round 1B
## Approach Explanation

### 1. Understanding the Problem

The goal of Round 1B is to build an intelligent document analyzer that extracts and ranks relevant sections from multiple documents based on a given persona and a specific task. In our case, the persona is a **Data Science Intern**, and the task is to **summarize key ML algorithms** from training material.

This setup simulates real-world document understanding, where context matters and not all content is equally relevant. Our solution is designed to generalize across different domains and personas.

---

### 2. Methodology

We followed a semantic similarity-based approach using the **Sentence Transformers** library to understand and compare text across different documents.

#### a. Input Preprocessing

- We collect all PDFs from the `input/` folder.
- Each document is read page by page using **PyMuPDF (fitz)**.
- The raw page text is split into paragraphs or chunks.
- Short or meaningless text (less than 5 words) is filtered out.

#### b. Persona and Task Encoding

- We read the persona and job-to-be-done from `persona.txt`.
- A combined prompt is created:  
  _“[Persona] needs to: [Task]”_
- This prompt is embedded using `paraphrase-MiniLM-L6-v2`, a lightweight and fast sentence transformer model suitable for CPU environments.

#### c. Ranking Logic

- Every extracted paragraph is embedded into a high-dimensional semantic vector.
- We compute cosine similarity between the prompt and each paragraph.
- Chunks are ranked based on similarity scores, ensuring the most relevant are selected.

#### d. Output Generation

- Top N (typically 10) most relevant sections are selected.
- For each result, we include:
  - Document name
  - Page number
  - A brief section title (first 60 characters of the chunk)
  - Importance rank
  - A subsection array with full extracted text

- All results are saved to `output/result.json` in the specified format.

---

### 3. Tools and Constraints

- **Model:** `paraphrase-MiniLM-L6-v2` (less than 100MB)
- **Runtime:** Fully offline, CPU-only
- **Execution Time:** < 60 seconds for 3–5 documents
- **Model Size:** < 1GB as required
- **Libraries Used:** PyMuPDF, SentenceTransformers, JSON, OS

---

### 4. Why This Approach?

- It generalizes across domains because no domain-specific rules or keywords are hardcoded.
- The use of sentence embeddings ensures deep semantic relevance, even when document phrasing is different from the prompt.
- The lightweight model ensures quick execution within the given constraints.

---

### 5. Conclusion

This solution provides a modular, general-purpose framework that can adapt to any persona or task by changing the `persona.txt` and input documents. It is efficient, extensible, and ready for production-like environments without requiring internet or GPUs.

