import re
from furet.traitement.getPdfText import *

# CLEANING FUNCTIONS ---------------------------------------------------------------------------------------

def cleanTitle(title):
    """Removes all newline characters and page numbers from an extracted document title"""
  
    cleanTitle = re.sub(' \\d{1,2}\\\n', ' ', title) #Remove page numbers
    cleanTitle = re.sub('\\\n', ' ', cleanTitle) #Remove leftover newlines
    return cleanTitle

def cleanType(docType):
    """Standardizes the document type"""

    docType = docType.lower()
    if re.search('arrêté|arreté|arrête|arrete|ap|am', docType):#Consider all representations of the word "decree"
        if re.search('municipal|am', docType):
            cleanType = 3
        elif re.search('préfectoral|prefectoral|ap', docType):
            cleanType = 2
        else:
            cleanType = 1

    elif re.search('consultation', docType) and re.search('publique', docType):
        cleanType = 4
    else:
        cleanType = 1

    return cleanType

# EXTRACTION FUNCTIONS ---------------------------------------------------------------------------------------

def extractPageCharacteristics(pageText, pageIndex):
    """Extracts clean data (number, title and type) from the text of a document"""

    regexp = f"- ((?:\\d|-)+) - ((\\S+) (?:.|\\n)+)" #This regexp extracts raw information from the decree footnote
    compiledRegexp = re.compile(regexp)
    matches = re.search(compiledRegexp, pageText)
  
    if matches: #If the footnote has been found
        groups = matches.groups() #Extract raw data from the footnote
        rawData = {"Number":groups[0], "Title":groups[1], "Type":groups[2].upper()}

        refined_data = {
            "Number":rawData["Number"],
            "Title":cleanTitle(rawData["Title"]), #The raw data is full of parasitic characters,
            "Type":cleanType(rawData["Type"])}    #we must clean it
        return refined_data

    else: #If no footnote, finding the data is too difficult (would require AI)
        return None


def extractDocumentCharacterisics(documentPath):
    """Converts a document to text and extracts its key data (number, title and type)"""

    textPages = extractPages(documentPath)

    extractedData = None
    characteristics = None

    #We try to extract information on the first page, then we repeat on other pages to correct potential errors.
    for pageIndex, pageText in enumerate(textPages):

        extractedData = extractPageCharacteristics(pageText, pageIndex)

        if pageIndex == 0 or extractedData is not None:
            characteristics = extractedData

    return characteristics