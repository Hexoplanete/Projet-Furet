import ocrmypdf

import os
from datetime import datetime

def create_searchable_pdf(input_pdf_path: str, output_pdf_path: str):
    """Apply OCR to the pdf "input_pdf_path" to generate a PDF with text "output_pdf_path" """
    ocrmypdf.ocr(
        input_pdf_path,
        output_pdf_path,
        language='fra',
        deskew=True,
        progress_bar=True,
        optimize=0,
        force_ocr=True,
    )

def process_file(input_pdf_path, output_pdf_path):
    """OCR and generation of searchable PDF."""

    print(f"\nInput PDF path: {input_pdf_path}")
    
    now = datetime.now()
    current_time = now.strftime("%H-%M-%S")
    
    print("Generating OCR PDF...")
    create_searchable_pdf(input_pdf_path, output_pdf_path)
    
    print(f"Output PDF path: {output_pdf_path}")

def main_ocr(input_path, output_pdf_path):
    """Processes one PDF or all PDFs in a folder."""
    if os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(input_path, filename)
                process_file(file_path, output_pdf_path)
    elif input_path.endswith(".pdf"):
        process_file(input_path,output_pdf_path)
    else:
        print("Invalid input. Please provide a PDF file or folder containing PDFs.")



