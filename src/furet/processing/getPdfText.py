import fitz

def extractText(inputPath, start_page=None, end_page=None):
    """
    Extracts the text between 2 pages (inclusive) of a PDF file. If no start and end pages are defined, then extracts the entire PDF text.

    Parameters:
        inputPath (str)             : Path to the input PDF file.
        start_page (int) (optional) : Page number to start extraction (0-based index). Defaults to the first page.
        end_page (int) (optional)   : Page number to end extraction (0-based index). Defaults to the last page.

    Returns:
        str: Extracted text from the specified page range, inclusive.
    """
    
    doc = fitz.open(inputPath)
    num_pages = len(doc)
    
    if start_page is None:
        start_page = 0
    if end_page is None:
        end_page = num_pages - 1

    if start_page < 0 or end_page >= num_pages or start_page > end_page:
        raise ValueError("The page numbers are invalid.")

    text = ""
    for pageNumber in range(start_page, end_page + 1):
        page = doc.load_page(pageNumber)
        text += page.get_text()
    
    return text
