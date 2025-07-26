# Adobe Challenge - Round 1A: Document Outline Extractor

## Task
Build a script that extracts a structured outline from a PDF file, including:
- Title (from PDF metadata or filename)
- Headings categorized as:
  - H1 (largest font or boldest headings)
  - H2
  - H3
Each heading also includes the page number.

## Libraries Used
- `PyMuPDF` (fitz) – for reading PDF content and font attributes
- `json` – for saving output in structured format
- `os` – for file handling

## Input and Output
- Input: One or more PDF files placed in the `input/` directory
- Output: Corresponding `.json` files with extracted outlines saved in the `output/` directory

## How to Run Locally (Without Docker)

1. Open a terminal or command prompt.
2. Navigate to the project directory:
   ```bash
   cd round1a
