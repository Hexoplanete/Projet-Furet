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

        # liste_output_path = []     # Liste qui contiendra les différents chemins vers les pdf des arrêté    
        # liste_objects_decree = []  # Liste qui contiendra les différents objets decrees
        liste_decrees = []           # Liste qui contiendra des listes [chemin, objet_decree]

        basename = os.path.basename(input_path).replace(".pdf","")

        doc = fitz.open(input_path)

        nb_pages = len(doc)

        full_text = ""
        for page in doc:
                full_text += page.get_text()

        print(nb_pages)
        print("-----------")

        # Remplacement artificiel des "s" et "S" par 5 car mauvaise reconnaissance de l'OCR !!!!!!
        full_text = full_text.replace("s","5")
        full_text = full_text.replace("S","5")

        # Extrait
        pages = re.findall(r'Page\s+(\d+)', full_text, flags=re.IGNORECASE)
        page_start_numbers = [int(p) for p in pages] 

        liste_chemin_objetDecree = []

        for i in range(len(page_start_numbers)):
                start = page_start_numbers[i]

                if(i == len(page_start_numbers) - 1): # Si on traite le dernier arrêté c'est différent car pas de i+1 !
                        end = nb_pages
                else:
                        end = page_start_numbers[i+1] - 1 # -2 car page_start_numbers[i+1] est le début du contenu du prochain, -1 est sa page de garde, -2 est la fin du courant

                # Création de l'objet arrêté

                arrete_id = 1 # Supprimer après merge
                #arrete_id = updateIdFile("decree")
                
                documentype = DocumentType(
                        id=0,
                        label="0"
                )

                campaign = Campaign(id=0, label="allo")

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
                        docType = documentype,
                        signingDate = date(2025, 5, 12),
                        campaign = campaign
                )

                current = []
                current.append(decree)

                # On ne connaît pas doc_type, number, title, signingDate, topic  à ce moment là (c'est dans extract caractéristiques) ni campaign (getKeyWords)
                # On ne connaît pas number à ce moment là (c'est dans extract caractéristiques)
                # On ne connaît pas title à ce moment là (c'est dans extract caractéristiques)
                # On ne connaît pas signingDate à ce moment là (c'est dans extract caractéristiques)
                # On ne connaît pas campaign à ce moment là (c'est dans getKeyWords)
                # On ne connaît pas topic  à ce moment là (c'est dans extract caractéristiques)

                sub_doc = fitz.open()

                sub_doc.insert_pdf(doc, from_page=start-1, to_page=end-1)

                output_path = os.path.join(output_dir, f"Arrete_{i+1}.pdf")

                current.append(output_path)
                #liste_output_path.append(output_path)

                liste_chemin_objetDecree.append(current)

                sub_doc.save(output_path)
                sub_doc.close()      

        return liste_chemin_objetDecree

