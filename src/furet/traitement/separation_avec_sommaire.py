from furet.types.decree import *
from database.config import *
from furet.repository import * 
from datetime import date

import fitz 
import re
from datetime import datetime
import os
import sys

def main_separation(input_path, output_dir, raa):
        now = datetime.now()
        current_time = now.strftime("%H-%M-%S")

        # liste_output_path = []     # List which will contain the different paths to the pdf of the decrees   
        # liste_objects_decree = []  # List that will contain the different decree objects
        liste_decrees = []           # List that will contain lists [chemin, objet_decree]

        basename = os.path.basename(input_path).replace(".pdf","")

        doc = fitz.open(input_path)

        nb_pages = len(doc)

        full_text = ""
        for page in doc:
                full_text += page.get_text()

        print(nb_pages)
        print("-----------")

        # Artificial replacement of "s" and "S" by 5 due to poor OCR recognition!!!!!!
        full_text = full_text.replace("s","5")
        full_text = full_text.replace("S","5")

        # Extract
        pages = re.findall(r'Page\s+(\d+)', full_text, flags=re.IGNORECASE)
        page_start_numbers = [int(p) for p in pages] 

        liste_chemin_objetDecree = []

        for i in range(len(page_start_numbers)):
                start = page_start_numbers[i]

                if(i == len(page_start_numbers) - 1): # If we process the last decree, it's different because there is no i+1!
                        end = nb_pages
                else:
                        end = page_start_numbers[i+1] - 1 # -2 because page_start_numbers[i+1] is the start of the next content, -1 is its cover page, -2 is the end of the current

                # Creation of the Decree object

                arrete_id = 1 # Deleted after merge
                #arrete_id = updateIdFile("decree")

                documenType = getDocumentTypeById(1)

                campaign = getCampaignById(1) # La campagne sera rédéfinie après les keywords

                decree = Decree(
                        id=arrete_id,
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

                sub_doc = fitz.open()

                sub_doc.insert_pdf(doc, from_page=start-1, to_page=end-1)

                output_path = os.path.join(output_dir, f"Arrete_{i+1}.pdf")

                current.append(output_path)

                liste_chemin_objetDecree.append(current)

                sub_doc.save(output_path)
                sub_doc.close()      

        return liste_chemin_objetDecree

