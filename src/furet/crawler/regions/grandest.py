from furet.crawler.spider import Spider
from bs4 import BeautifulSoup
from datetime import datetime
import os
import requests

class Moselle(Spider):
    """
    A spider class for crawling the Moselle department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, ouputDir, configFile, linkFile, date):
        """
        Initialize the Moselle spider with specific parameters.
        """
        super().__init__(ouputDir, configFile, linkFile, date)
        self.baseURL = "https://mc.moselle.gouv.fr/raa.html?adminedit=1?op=raa&do=raa_rec&page="
        self.region = "GrandEst"
        self.department = "Moselle"
        self.currentMostRecentRAA = self.mostRecentRAA
        
    def extractLinks(self, html):
        """
        Extract all links from the HTML content.

        :param html: HTML content of a page.
        :return: List of extracted links.
        """
        soup = BeautifulSoup(html, 'html.parser')
        extractedData = []
        rows = soup.find_all('tr', class_=['li1', 'li2'])

        for row in rows:
            if not "javascript:void(0);" in str(row):
                continue
            try:
                dateStr = row.find_all('td')[2].text.strip() if len(row.find_all('td')) >= 4 else None # Extract the date from the row
                if not dateStr:
                    continue
                date = datetime.strptime(dateStr, "%d/%m/%Y")

                linkTag = row.find_all('a', href=True)[1] if len(row.find_all('td')) >= 2 else None     # Extract the link from the row
                if not linkTag:
                    continue

                if date > self.mostRecentRAA:             # If the date is more recent than the most recent RAA, add it to the list
                    link = linkTag['href']
                    extractedData.append({"link": link, "datePublication": dateStr, "region": self.region, "department": self.department})
                    if date > self.currentMostRecentRAA:
                        self.currentMostRecentRAA = date
            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return extractedData
    
    def downloadPDF(self, url):
        """
        Download a PDF file from the given URL and put it in the output directory.

        :param url: URL of the PDF file.
        """
        try:
            response = requests.get(url, stream=True, headers=self.headers)
            response.raise_for_status()
            
            filename = os.path.join(self.ouputDir, url[-10:])
            if not filename.endswith('.pdf'):
                filename += ".pdf"
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Downloaded: {filename}")
        except requests.RequestException as e:
            print(f"Failed to download {url}: {e}")
        
    def crawl(self):
        """
        Crawl the website to find and download the most recent RAA links.
        """
        try:
            i = 1
            finalLinks = []
            while True:           # Loop through the pages until no more links are found
                url = self.baseURL + str(i)
                i += 1
                html = self.fetchPage(url)
                if not html or "Il n'y a aucun recueil cr" in html: # Check if the page is empty or if there are no more RAA
                    break

                links = self.extractLinks(html)
                if links == []:     # if no more links are found, break the loop because every subsequent RAA will be too old
                    break

                for link in links:
                    finalLinks.append(link)
            
            if self.currentMostRecentRAA > self.mostRecentRAA:  
                self.mostRecentRAA = self.currentMostRecentRAA
                self.setMostRecentRAADate(self.mostRecentRAA, self.region, self.department)

            self.addToJsonResultFile(finalLinks)

        except Exception as e:
            print(f"Error during crawling in {self.department}: {e}")
            return None
        
        return finalLinks
