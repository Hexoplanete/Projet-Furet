import threading
import time
from furet.crawler.crawler import Crawler

def init():
    start_time = time.time()
    crawler = Crawler()
    crawler_thread = threading.Thread(target=crawler.startCrawler)

    crawler_thread.start()

    crawler_thread.join()
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

    # processing = Traitement()
    # processing_thread = threading.Thread(target=processing.startTraitement)
    # processing_thread.start()