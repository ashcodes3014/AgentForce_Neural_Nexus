from PyPDF2 import PdfReader
from typing import Tuple


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
    except Exception as e:
        raise ValueError(f"Failed to process PDF: {str(e)}")

def process_resume_text(text: str) -> Tuple[str, list[str]]:
    """Process extracted text into chunks"""
    chunks = [text[i:i+1000] for i in range(0, len(text), 800)]
    return text, chunks