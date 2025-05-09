import furet.app
from furet.crawler.crawler import Crawler
import threading


def main():
    crawler = Crawler()
    crawler_thread = threading.Thread(target=crawler.startCrawler)
    app_thread = threading.Thread(target=furet.app.main)

    crawler_thread.start()
    app_thread.start()

    crawler_thread.join()
    app_thread.join()

if __name__ == '__main__':
    print("Running as main module.")
    main()