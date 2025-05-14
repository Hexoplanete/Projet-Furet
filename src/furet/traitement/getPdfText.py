import fitz 

def extractText(inputPath):
    doc = fitz.open(inputPath)

    text = ""

    for pageNumber in range(len(doc)):
        page = doc.load_page(pageNumber)
        text += page.get_text()
    
    return text

def extractPages(input_path):
    doc = fitz.open(input_path)

    textPages = []

    for pageNumber in range(len(doc)):
        page = doc.load_page(pageNumber)
        textPages.append(page.get_text())
    
    return textPages