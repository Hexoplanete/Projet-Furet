from furet import repository
from furet.types.decree import *
from furet.processing.getPdfText import extractText
from datetime import date

import fitz
import re
from datetime import datetime
import os


def mainSeparation(inputPath, outputDir, raa: RAA) -> list[tuple[str, Decree]]:
    now = datetime.now()
    currentTime = now.strftime("%H-%M-%S")

    # listeOutputPath = []     # List which will contain the different paths to the pdf of the decrees
    # listeObjectsDecree = []  # List that will contain the different decree objects
    listeDecrees = []           # List that will contain lists [chemin, objetDecree]

    baseName = os.path.basename(inputPath).replace(".pdf", "")

    doc = fitz.open(inputPath)

    nbPages = len(doc)

    raaTextContent = ""
    for page in doc:
        raaTextContent += page.get_text()

    # print(nbPages)
    # print("-----------")

    # Artificial replacement of "s" and "S" by 5 due to poor OCR recognition!!!!!!
    # The separation is made with the summary of the decree (page numbers) in it so it is absolutely necessary that the numbers are correct!!!
    raaTextContent = raaTextContent.replace("s", "5")
    raaTextContent = raaTextContent.replace("S", "5")

    # Extract
    pages = re.findall(r'Page\s+(\d+)', raaTextContent, flags=re.IGNORECASE)
    pageStartNumbers = [int(p) for p in pages]

    decrees: list[tuple[str, Decree]] = []

    for i in range(len(pageStartNumbers)):
        start = pageStartNumbers[i]

        # If we process the last decree, it's different because there is no i+1!
        if (i == len(pageStartNumbers) - 1):
            end = nbPages
        else:
            # -2 because page_start_numbers[i+1] is the start of the next content, -1 is its cover page, -2 is the end of the current
            end = pageStartNumbers[i+1] - 1

        # The text of the decree is extracted
        # Change extract text so that it returns a dictionary like that when we retrieve all the text before, we don't have to do it again there!
        # decreeTextContent = extractText(inputPath, start_page=start-1, end_page=end-1)

        # Creation of the Decree object
        decree = Decree(
            id=0,
            raa=raa,
            startPage=start,
            endPage=end,
        )

        # We don't know doc_type, number, title, signingDate, topic at this time (it's in extract characteristics) nor campaign (getKeyWords)
        # We don't know number at this time (it's in extract characteristics)
        # We don't know title at this time (it's in extract characteristics)
        # We don't know signingDate at this time (it's in extract characteristics)
        # We don't know campaign at this time (it's in getKeyWords)
        # We don't know topic at this time (it's in extract characteristics)

        outputPath = os.path.join(outputDir, f"Arrete_{i+1}.pdf")
        subDoc = fitz.open()
        subDoc.insert_pdf(doc, from_page=start-1, to_page=end-1)
        subDoc.save(outputPath)
        subDoc.close()

        decrees.append((outputPath, decree))

    return decrees
