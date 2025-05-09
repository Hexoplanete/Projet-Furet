import fitz 
import re
from datetime import datetime
import os
import sys


def main_separation(input_path, output_dir):
        now = datetime.now()
        current_time = now.strftime("%H-%M-%S")

        liste_output_path = [] # Liste qui contiendra les différents chemins vers les pdf des arrêtés

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

        for i in range(len(page_start_numbers)):
                start = page_start_numbers[i]

                if(i == len(page_start_numbers) - 1): # Si on traite le dernier arrêté c'est différent car pas de i+1 !
                        end = nb_pages
                else:
                        end = page_start_numbers[i+1] - 1 # -2 car page_start_numbers[i+1] est le début du contenu du prochain, -1 est sa page de garde, -2 est la fin du courant

                sub_doc = fitz.open()

                sub_doc.insert_pdf(doc, from_page=start-1, to_page=end-1)

                output_path = os.path.join(output_dir, f"Arrete_{i+1}.pdf")

                liste_output_path.append(output_path)

                sub_doc.save(output_path)
                sub_doc.close()      

        return liste_output_path 

