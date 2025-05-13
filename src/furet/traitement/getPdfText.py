import fitz 

def extractText(inputPath):
    doc = fitz.open(inputPath)

    text = ""

    for pageNumber in range(len(doc)):
        page = doc.load_page(pageNumber)
        text += page.get_text()
    
    return text