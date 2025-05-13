from furet.types.decree import *
from database.config import *
from furet.repository import * 
from datetime import date

import fitz 
import re
from datetime import datetime
import os
import sys

def mainSeparation(inputPath, outputDir, raa):
        now = datetime.now()
        currentTime = now.strftime("%H-%M-%S")

        # listeOutputPath = []     # List which will contain the different paths to the pdf of the decrees   
        # listeObjectsDecree = []  # List that will contain the different decree objects
        listeDecrees = []           # List that will contain lists [chemin, objetDecree]

        baseName = os.path.basename(inputPath).replace(".pdf","")

        doc = fitz.open(inputPath)

        nbPages = len(doc)

        fullText = ""
        for page in doc:
                fullText += page.get_text()

        print(nbPages)
        print("-----------")

        # Artificial replacement of "s" and "S" by 5 due to poor OCR recognition!!!!!!
        fullText = fullText.replace("s","5")
        fullText = fullText.replace("S","5")

        # Extract
        pages = re.findall(r'Page\s+(\d+)', fullText, flags=re.IGNORECASE)
        pageStartNumbers = [int(p) for p in pages] 

        listeCheminObjetDecree = []

        for i in range(len(pageStartNumbers)):
                start = pageStartNumbers[i]

                if(i == len(pageStartNumbers) - 1): # If we process the last decree, it's different because there is no i+1!
                        end = nbPages
                else:
                        end = pageStartNumbers[i+1] - 1 # -2 because page_start_numbers[i+1] is the start of the next content, -1 is its cover page, -2 is the end of the current

                # Creation of the Decree object

                arreteId = 1 # Deleted after merge
                #arreteId = updateIdFile("decree")

                documenType = getDocumentTypeById(1)

                campaign = getCampaignById(1) # La campagne sera rédéfinie après les keywords

                decree = Decree(
                        id=arreteId,
                        department=raa.department,
                        raaNumber=raa.number,                   # On ne connaît pas raaNumber à ce moment là (c'est dans extract caractéristiques)
                        link=raa.link,
                        startPage=start, 
                        endPage=end,
                        treated=False,
                        comment="0",
                        publicationDate=raa.publicationDate,
                        docType = documenType,
                        signingDate = date(2025, 5, 12),
                        campaign = campaign
                )

                current = []
                current.append(decree)

                # We don't know doc_type, number, title, signingDate, topic at this time (it's in extract characteristics) nor campaign (getKeyWords)
                # We don't know number at this time (it's in extract characteristics)
                # We don't know title at this time (it's in extract characteristics)
                # We don't know signingDate at this time (it's in extract characteristics)
                # We don't know campaign at this time (it's in getKeyWords)
                # We don't know topic at this time (it's in extract characteristics)

                subDoc = fitz.open()

                subDoc.insert_pdf(doc, from_page=start-1, to_page=end-1)

                outputPath = os.path.join(outputDir, f"Arrete_{i+1}.pdf")

                current.append(outputPath)

                listeCheminObjetDecree.append(current)

                subDoc.save(outputPath)
                subDoc.close()      

        return listeCheminObjetDecree

