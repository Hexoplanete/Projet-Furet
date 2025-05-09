import fitz 

def extract_text(input_path):
    doc = fitz.open(input_path)

    text = ""

    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        text += page.get_text()
    
    return text