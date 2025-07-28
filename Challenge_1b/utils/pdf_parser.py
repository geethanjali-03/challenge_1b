import fitz  # PyMuPDF

def extract_text_from_pdfs(pdf_paths):
    pdf_data = {}

    for pdf_path in pdf_paths:
        doc = fitz.open(pdf_path)
        pages = [page.get_text() for page in doc]  # List of page-wise text
        pdf_data[pdf_path.name] = pages  # Key = filename (e.g., "file1.pdf")

    return pdf_data

