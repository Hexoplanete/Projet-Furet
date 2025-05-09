import furet.app
from furet.crawler.crawler import Crawler
from furet import repository
import threading
import time

#from datetime import datetime

def main():
    repository.setup()
    # crawler = Crawler()
    # crawler.startCrawler()
    furet.app.main()
    start_time = time.time()
    crawler = Crawler()
    crawler_thread = threading.Thread(target=crawler.startCrawler)
    app_thread = threading.Thread(target=furet.app.main)

    crawler_thread.start()
    app_thread.start()

    crawler_thread.join()
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

    # traitement = Traitement()
    # traitement_thread = threading.Thread(target=traitement.startTraitement)
    # traitement_thread.start()

    app_thread.join()

if __name__ == '__main__':
    main()
    