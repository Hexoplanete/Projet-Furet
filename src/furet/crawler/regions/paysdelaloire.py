from furet.crawler.spider import Spider
from bs4 import BeautifulSoup
from datetime import datetime
import requests

class Sarthe(Spider):
    """
    A spider class for crawling the Sarthe department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the Moselle spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseUrl = "https://www.sarthe.gouv.fr/Publications/Recueils-des-actes-administratifs"
        self.region = "PaysDeLaLoire"
        self.department = "Sarthe"
        self.currentMostRecentRAA = self.mostRecentRAA

    def postSelectedYear(self, year):
        """
        Select a specific year by simulating a POST request to refresh the page.

        :param year: The year to select.
        :return: HTML content of the refreshed page.
        """
        headers = {     # Simulate a POST request to select the year, mimicking a browser
            "Content-Length": "72",
            "Cache-Control": "max-age=0",
            "Sec-Ch-Ua": "\"Chromium\";v=\"135\", \"Not-A.Brand\";v=\"8\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Accept-Language": "fr-FR,fr;q=0.9",
            "Origin": "https://www.sarthe.gouv.fr",
            "Content-Type": "application/x-www-form-urlencoded",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://www.sarthe.gouv.fr/Publications/Recueils-des-actes-administratifs",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=0, i"
        }
        payload = f"Liste-liste-docs=Publications%2FRecueils-des-actes-administratifs%2F{year}"
        
        response = requests.post(self.baseUrl, data=payload, headers=headers) # Simulate a POST request to select the year
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to select year {year}. Status code: {response.status_code}")
            return None
        
    def findPages(self, html):
        """
        Find the number of pages available in the HTML content.

        :param html: HTML content of a page.
        :return: Number of pages found.
        """
        extractedPages = []
        soup = BeautifulSoup(html, 'html.parser')         
        RAAYears = soup.find_all('option', value=True, title=True) # Find all options with a value and title attribute
        for year in RAAYears:
            yearValue = year['title']
            if int(yearValue) < self.mostRecentRAA.year: # If the year is older than the most recent RAA, skip it
                break
            htmlContent = self.postSelectedYear(yearValue)
            extractedPages.append(htmlContent)

        return extractedPages
        
    def extractLinks(self, html, links):
        """
        Extract all links from the HTML content.

        :param html: HTML content of a page.
        :return: List of extracted links.
        """
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('a', class_="fr-link fr-link--download")

        for row in rows:
            try:
                dateStr = row.find('span', class_='fr-link__detail').text.split()[-1] # Extract the date from the link text
                date = datetime.strptime(dateStr, "%d/%m/%Y")

                if date > self.mostRecentRAA:           # If the date is more recent than the most recent RAA, add it to the list
                    link = row['href']
                    links.append({"link": 'https://www.sarthe.gouv.fr' + link, "datePublication": dateStr, "region": self.region, "department": self.department}) # Add the link to the list for JSON output
                    if date > self.currentMostRecentRAA:
                        self.currentMostRecentRAA = date

            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return links
    
        
    def crawl(self):
        try:           
            htmlPages = self.findPages(self.fetchPage(self.baseUrl)) # For each year, there is a page with RAAs
            links = []
            for htmlPage in htmlPages:
                if not htmlPage:
                    break

                self.extractLinks(htmlPage, links)
            
            if self.currentMostRecentRAA > self.mostRecentRAA: # If a more recent RAA is found, update the most recent RAA
                self.mostRecentRAA = self.currentMostRecentRAA
                self.setMostRecentRAADate(self.mostRecentRAA, self.region, self.department)

            self.addToJsonResultFile(links) # Add the links to the JSON result file

        except Exception as e:
            print(f"Error during crawling: {e}")
            return None
        
        return self.mostRecentRAA
