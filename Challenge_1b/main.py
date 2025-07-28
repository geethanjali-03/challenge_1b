from pathlib import Path
import os
import sys
import json
from datetime import datetime

from utils.pdf_parser import extract_text_from_pdfs
from src.llm_engine import get_relevant_sections


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <path_to_PDFs_folder> <path_to_persona_file>")
        sys.exit(1)

    input_folder = Path(sys.argv[1])  # e.g., Collection 1/PDFs
    persona_file = Path(sys.argv[2])  # e.g., personas/persona1.txt

    if not input_folder.exists() or not input_folder.is_dir():
        print(f"Invalid PDFs folder: {input_folder}")
        sys.exit(1)

    if not persona_file.exists():
        print(f"Persona file not found: {persona_file}")
        sys.exit(1)

    # Collect all PDF paths
    pdf_paths = sorted(input_folder.glob("*.pdf"), key=lambda x: x.name.lower())
    if not pdf_paths:
        print(f"No PDF files found in {input_folder}")
        sys.exit(1)

    # Extract text from PDFs
    pdf_data = extract_text_from_pdfs(pdf_paths)
    print("DEBUG: Type of pdf_data =", type(pdf_data))

    # Read persona and job-to-be-done
    with open(persona_file, "r", encoding="utf-8") as f:
        persona_job = f.read()

    lines = persona_job.strip().split("\n")
    persona = lines[0].strip()
    job = " ".join(lines[1:]).strip()

    print("🔍 Calling LLM...")
    try:
        result = get_relevant_sections(pdf_data, persona_job=persona, max_sections=5, job_to_be_done=job)
        print("LLM call succeeded")
    except Exception as e:
        print("LLM call failed:", e)
        sys.exit(1)

    # Build output JSON
    output_json = {
        "metadata": {
            "input_documents": [p.name for p in pdf_paths],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": result.get("extracted_sections", []),
        "subsection_analysis": result.get("subsection_analysis", {})
    }

    # Determine output path: Collection X/challenge1b_output.json
    collection_folder = input_folder.parent
    output_path = collection_folder / "challenge1b_output.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_json, f, indent=2, ensure_ascii=False)

    print(f"Output written to {output_path}")


if __name__ == "__main__":
    main()

