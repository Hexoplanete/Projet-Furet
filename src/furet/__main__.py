import sys
import furet.app
from furet.crawler.Crawler import Crawler


def main():
    print("Starting Furet...")
    crawler = Crawler()
    print("Crawler initialized.")
    crawler.startCrawler()
    print("Crawler started.")
    furet.app.main()

if __name__ == '__main__':
    print("Running as main module.")
    main()