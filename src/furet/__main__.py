import furet.app
from furet.crawler.crawler import Crawler
from furet import repository
import threading

#from datetime import datetime

def main():
    repository.setup()
    # crawler = Crawler()
    # crawler.startCrawler()
    furet.app.main()

if __name__ == '__main__':
    main()
    