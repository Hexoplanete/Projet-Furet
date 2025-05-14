import threading
import time
from furet.crawler.crawler import Crawler
from furet import settings


def setup():
    settings.setDefaultValue("crawler.autorun", False)
    
    autorun = settings.value("crawler.autorun")
    if autorun:
        from furet.traitement.processing import Traitement
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