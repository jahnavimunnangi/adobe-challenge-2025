import os
import fitz  # PyMuPDF
import json

# Known heading keywords in various languages
MULTILINGUAL_HEADINGS = [
    "はじめに",  # Japanese: Introduction
    "目次",      # Japanese: Table of Contents
    "परिचय",     # Hindi: Introduction
    "内容",      # Chinese: Content
    "绪论",      # Chinese: Preface
    "導入",      # Japanese: Introduction
    "개요",      # Korean: Overview
]

def is_multilingual(text):
    """Check if a line contains non-ASCII characters (Unicode)"""
    return any(ord(char) > 127 for char in text)

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []

    # Use title from metadata or fallback to filename
    title = doc.metadata.get("title") or os.path.basename(pdf_path)
    print(f"\nProcessing document: {title}")

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                spans = line.get("spans", [])
                if not spans:
                    continue

                # Combine all spans in the line
                line_text = " ".join(span["text"] for span in spans).strip()
                if not line_text:
                    continue

                font_sizes = [span["size"] for span in spans if span["text"].strip()]
                font_size = max(font_sizes) if font_sizes else 0

                font_flags = [span.get("flags", 0) for span in spans]
                is_bold = any(flag & 2 for flag in font_flags)

                contains_unicode = is_multilingual(line_text)

                # Heading heuristics
                is_heading_by_style = font_size >= 13 or (font_size >= 11 and is_bold)
                is_heading_by_keyword = any(kw in line_text for kw in MULTILINGUAL_HEADINGS)

                if is_heading_by_style or is_heading_by_keyword:
                    if font_size >= 16:
                        level = "H1"
                    elif font_size >= 13:
                        level = "H2"
                    else:
                        level = "H3"

                    outline.append({
                        "level": level,
                        "text": line_text,
                        "page": page_num
                    })

    return {
        "title": title,
        "outline": outline
    }

def process_folder(input_dir, output_dir):
    print(f"\nScanning folder: {input_dir}")
    if not os.path.exists(input_dir):
        print("Error: Input folder does not exist.")
        return

    os.makedirs(output_dir, exist_ok=True)

    pdf_files = [file for file in os.listdir(input_dir) if file.lower().endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDF(s): {pdf_files}")

    for file in pdf_files:
        pdf_path = os.path.join(input_dir, file)
        print(f"Extracting outline from: {file}")
        result = extract_outline(pdf_path)

        output_file = os.path.join(output_dir, file.replace(".pdf", ".json"))
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"Saved output to: {output_file}")

if __name__ == "__main__":
    input_dir = "input"
    output_dir = "output"
    process_folder(input_dir, output_dir)
