import requests
import fitz  # PyMuPDF

def download_pdf(pdf_url, output_path):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open(output_path, "wb") as file:
            file.write(response.content)
        return output_path
    else:
        raise Exception(f"Failed to download PDF from {pdf_url}, status code {response.status_code}")

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text
