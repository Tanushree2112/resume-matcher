import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(r"C:\Users\tapar\OneDrive\Desktop\cv1.pdf") as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text
