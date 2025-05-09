import sys
import furet.app
from furet.crawler.crawler import Crawler
from furet import repository

def main():
    repository.setup(repository.allDecreeList)
    # crawler = Crawler()
    # crawler.startCrawler()
    furet.app.main()

if __name__ == '__main__':
    main()
    