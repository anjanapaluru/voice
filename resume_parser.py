import PyPDF2

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from an uploaded PDF file.
    """
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return None

def summarize_resume(text):
    """
    Basic summary of resume text to feed into Gemini.
    In this app, we'll pass the full text, but this helper can be used to trim if needed.
    """
    if not text:
        return "No resume provided."
    
    # Just returning first 5000 characters for demo simplicity
    return text[:5000]
