import requests
from datetime import datetime
import os
import json
from time import sleep
from random import uniform
from furet import settings
import ast

class Spider:
    """
    Base class for web crawlers to fetch and process data from government websites.
    This class provides methods to fetch pages, extract links, and download PDF files.
    It is designed to be subclassed for specific regions and departments.
    """
    def __init__(self, outputDir, configFile="./configCrawler.json", linkFile="./resultCrawler.json", date="01/01/2025"):
        self.outputDir = outputDir
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "fr-FR,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }
        self.mostRecentRAA = datetime.strptime(date, "%d/%m/%Y")
        self.configFile = settings.value("crawler.config")
        self.linkFile = linkFile
        self.baseUrl = None
        self.months = {
            "janvier": 1,
            "février": 2,
            "fevrier": 2,
            "mars": 3,
            "avril": 4,
            "mai": 5,
            "juin": 6,
            "juillet": 7,
            "août": 8,
            "aout": 8,
            "septembre": 9,
            "octobre": 10,
            "novembre": 11,
            "décembre": 12,
            "decembre": 12
        }
    
    def setMostRecentRAADate(self, date, region, department):
        """
        Set the most recent RAA date in the configuration file.

        :param configFile: Path to the configuration file.
        :param date: Date to set.
        """
        try:
            data = ast.literal_eval(settings.value("crawler.config"))
            data["regions"][region]["departments"][department] = date.strftime("%d/%m/%Y")
            test = str(data)
            settings.setValue("crawler.config", str(data))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error writing to config file: {e}")

    def fetchPage(self, url):
        """
        Fetch the content of a webpage with headers mimicking a browser.

        :param url: URL of the webpage to fetch.
        :return: HTML content of the page.
        """
        try:
            sleep(uniform(1, 3))  # Sleep for a random duration between 0.5 and 1.5 seconds to avoid overwhelming the server
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            return None

    def downloadPDF(self, url):
        """
        Download a PDF file from the given URL and put it in the output directory.

        :param url: URL of the PDF file.
        """
        try:
            response = requests.get(url, stream=True, headers=self.headers)
            response.raise_for_status()
            
            filename = os.path.join(self.output_dir, url.split('/')[-1])
            if not filename.endswith('.pdf'):
                filename += ".pdf"
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Downloaded: {filename}")
        except requests.RequestException as e:
            print(f"Failed to download {url}: {e}")

    def addToJsonResultFile(self, linkList):
        """
        Add the extracted links to the JSON result file.
        """
        with open(self.linkFile, "r") as f:
            data = json.load(f)
            data["links"].extend(linkList)
        with open(self.linkFile, "w") as f:
            json.dump(data, f, indent=4) 

    def crawl(self):
        """
        Crawl the website to find and download the most recent RAA links.
        """
        try:
            linksPages = self.findPages(self.fetchPage(self.baseUrl)) 
            links = []
            for link in linksPages:

                html = self.fetchPage(link)
                if not html:
                    break

                self.extractLinks(html, links)

            # Update the most recent RAA if a newer one is found
            if self.currentMostRecentRAA > self.mostRecentRAA: 
                self.mostRecentRAA = self.currentMostRecentRAA
                self.setMostRecentRAADate(self.mostRecentRAA, self.region, self.department)

            self.addToJsonResultFile(links)

        except Exception as e:
            print(f"Error during crawling in {self.department}: {e}")
            return None
        
        return links
        