import threading
import time
from furet.crawler.crawler import Crawler
from furet import settings
from furet.traitement.processing import Traitement


def setup():
    settings.setDefaultValue("crawler.autorun", False)
    
    autorun = settings.value("crawler.autorun"); 
    
    settings.setDefaultValue("crawler.config", '{ "regions": { "GrandEst": { "departments": { "Aube": "09/05/2025" } }, "Occitanie": { "departments": { "HautesPyrenees": "11/05/2025", "Ariege": "09/05/2025", "Gers": "07/05/2025" } }, "PACA": { "departments": { "AlpesMaritimes": "09/05/2025", "Var": "09/05/2025", "BouchesDuRhone": "13/05/2025", "AlpesDeHauteProvence": "12/05/2025" } }, "AURA": { "departments": { "Allier": "13/05/2025" } }, "NouvelleAquitaine": { "departments": { "Charente": "05/05/2025" } }, "PaysDeLaLoire": { "departments": { "Sarthe": "13/05/2025" } }, "BourgogneFrancheComte": { "departments": { "SaoneEtLoire": "13/05/2025", "Doubs": "09/05/2025", "Jura": "07/05/2025" } }, "HautsDeFrance": { "departments": { "Nord": "07/05/2025", "PasDeCalais": "09/05/2025", "Somme": "09/05/2025" } }, "Normandie": { "departments": { "Calvados": "13/05/2025" } }, "Bretagne": { "departments": { "CotesDArmor": "07/05/2025", "Morbihan": "09/05/2025" } }, "CentreValDeLoire": { "departments": { "Loiret": "09/05/2025", "Indre": "09/05/2025", "Cher": "09/05/2025" } } } } }')
    
    settings.setValue("crawler.config", '{ "regions": { "GrandEst": { "departments": { "Aube": "09/05/2025" } }, "Occitanie": { "departments": { "HautesPyrenees": "11/05/2025", "Ariege": "09/05/2025", "Gers": "07/05/2025" } }, "PACA": { "departments": { "AlpesMaritimes": "09/05/2025", "Var": "09/05/2025", "BouchesDuRhone": "13/05/2025", "AlpesDeHauteProvence": "12/05/2025" } }, "AURA": { "departments": { "Allier": "13/05/2025" } }, "NouvelleAquitaine": { "departments": { "Charente": "05/05/2025" } }, "PaysDeLaLoire": { "departments": { "Sarthe": "13/05/2025" } }, "BourgogneFrancheComte": { "departments": { "SaoneEtLoire": "13/05/2025", "Doubs": "09/05/2025", "Jura": "07/05/2025" } }, "HautsDeFrance": { "departments": { "Nord": "07/05/2025", "PasDeCalais": "09/05/2025", "Somme": "09/05/2025" } }, "Normandie": { "departments": { "Calvados": "13/05/2025" } }, "Bretagne": { "departments": { "CotesDArmor": "07/05/2025", "Morbihan": "09/05/2025" } }, "CentreValDeLoire": { "departments": { "Loiret": "09/05/2025", "Indre": "09/05/2025", "Cher": "09/05/2025" } } } }')

    if True:
        start_time = time.time()
        crawler = Crawler()
        crawler_thread = threading.Thread(target=crawler.startCrawler)

        crawler_thread.start()

        crawler_thread.join()
        end_time = time.time()
        print(f"Total execution time: {end_time - start_time:.2f} seconds")

        traitement = Traitement()
        traitement_thread = threading.Thread(target=traitement.startTraitement)
        traitement_thread.start()
        traitement_thread.join()