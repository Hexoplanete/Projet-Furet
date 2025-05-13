import ocrmypdf

import os
from datetime import datetime

def createSearchable_pdf(inputPath_pdf: str, outputPath_pdf: str):
    """Apply OCR to the pdf "inputPath_pdf" to generate a PDF with text "outputPath_pdf" """
    ocrmypdf.ocr(
        inputPath_pdf,
        outputPath_pdf,
        language='fra',
        deskew=True,
        progressBar=True,
        optimize=0,
        forceOcr=True,
    )

def processFile(inputPath_pdf, outputPath_pdf):
    """OCR and generation of searchable PDF."""

    print(f"\nInput PDF path: {inputPath_pdf}")
    
    now = datetime.now()
    currentTime = now.strftime("%H-%M-%S")
    
    print("Generating OCR PDF...")
    createSearchable_pdf(inputPath_pdf, outputPath_pdf)
    
    print(f"Output PDF path: {outputPath_pdf}")

def mainOcr(inputPath, outputPath_pdf):
    """Processes one PDF or all PDFs in a folder."""
    if os.path.isdir(inputPath):
        for fileName in os.listdir(inputPath):
            if fileName.endswith(".pdf"):
                filePath = os.path.join(inputPath, fileName)
                processFile(filePath, outputPath_pdf)
    elif inputPath.endswith(".pdf"):
        processFile(inputPath,outputPath_pdf)
    else:
        print("Invalid input. Please provide a PDF file or folder containing PDFs.")



