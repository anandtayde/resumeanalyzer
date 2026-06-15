import io
import pypdf
import docx2txt

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts text from PDF file bytes using pypdf."""
    pdf_file = io.BytesIO(file_bytes)
    reader = pypdf.PdfReader(pdf_file)
    text = ""
    for page_num, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extracts text from DOCX file bytes using docx2txt."""
    docx_file = io.BytesIO(file_bytes)
    # docx2txt.process requires a file path or a file-like object
    text = docx2txt.process(docx_file)
    return text.strip()

def parse_resume(uploaded_file) -> str:
    """
    Parses a Streamlit UploadedFile object and extracts text.
    Supports PDF, DOCX, and TXT formats.
    """
    file_name = uploaded_file.name.lower()
    file_bytes = uploaded_file.read()
    
    # Reset file pointer for potential future reads in streamlit
    uploaded_file.seek(0)
    
    if file_name.endswith('.pdf'):
        return extract_text_from_pdf(file_bytes)
    elif file_name.endswith('.docx') or file_name.endswith('.doc'):
        return extract_text_from_docx(file_bytes)
    elif file_name.endswith('.txt'):
        try:
            return file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return file_bytes.decode('latin-1')
    else:
        raise ValueError(f"Unsupported file type: {uploaded_file.name}. Please upload PDF, DOCX, or TXT.")
