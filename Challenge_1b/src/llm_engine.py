import re 
from datetime import datetime
def get_relevant_sections(pdf_data, max_sections=5, persona_job=None, job_to_be_done=None):
    """
    Extract relevant sections from PDFs by selecting pages with meaningful text,
    filtered by persona job relevance (optional), with metadata and better titles.

    Args:
        pdf_data: dict of {document_name: [page_texts]}
        max_sections: int, max number of sections to return
        persona_job: optional string for extra prompt context
        job_to_be_done: optional string describing the task/context

    Returns:
        dict with metadata, extracted_sections, and subsection_analysis.
    """

    def is_relevant(text, keywords):
        # If no keywords provided, accept all texts as relevant
        if not keywords:
            return True
        text_lower = text.lower()
        return any(k in text_lower for k in keywords)

    def extract_title(text):
        # Try to find a meaningful title line:
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if not lines:
            return "No Title"
        for line in lines[:5]:
            if 5 < len(line) <= 100:
                words = line.split()
                cap_words = sum(1 for w in words if w[0].isupper())
                if cap_words >= max(1, len(words)//2):
                    return line
        return lines[0]

    def summarize_text(text, max_chars=800):
        # Simple summarization: first few sentences until max_chars
        sentences = re.split(r'(?<=[.!?]) +', text)
        summary = ""
        for sent in sentences:
            if len(summary) + len(sent) > max_chars:
                break
            summary += sent + " "
        return summary.strip()

    # Extract keywords from persona_job if provided, else empty list = accept all pages
    persona_keywords = re.findall(r'\w+', persona_job.lower()) if persona_job else []

    all_sections = []
    all_subsections = []

    for doc, pages in pdf_data.items():
        for i, page_text in enumerate(pages):
            text = page_text.strip()
            if len(text) < 50:
                # Skip very short pages
                continue
            if is_relevant(text, persona_keywords):
                title = extract_title(text)
                refined = summarize_text(text)

                all_sections.append({
                    "document": doc,
                    "section_title": title,
                    "importance_metric": len(text),
                    "page_number": i + 1
                })
                all_subsections.append({
                    "document": doc,
                    "refined_text": refined,
                    "page_number": i + 1
                })

    # Sort by length of text (descending) as proxy for importance
    all_sections = sorted(all_sections, key=lambda s: s["importance_metric"], reverse=True)

    # Limit number of sections returned
    selected_sections = all_sections[:max_sections]

    # Assign importance_rank and remove importance_metric
    for idx, sec in enumerate(selected_sections, start=1):
        sec["importance_rank"] = idx
        sec.pop("importance_metric", None)

    # Align subsections with selected sections
    selected_subsections = []
    for sec in selected_sections:
        for sub in all_subsections:
            if sub["document"] == sec["document"] and sub["page_number"] == sec["page_number"]:
                selected_subsections.append(sub)
                break
    for section in selected_sections:
        if "page_number" in section:
            page = section.pop("page_number")
            section["page_number"] = page
    metadata = {
        "input_documents": list(pdf_data.keys()),
        "persona": persona_job or "",
        "job_to_be_done": job_to_be_done or "",
        "processing_timestamp": datetime.now().isoformat()
    }

    return {
        "metadata": metadata,
        "extracted_sections": selected_sections,
        "subsection_analysis": selected_subsections
    }
