from furet.crawler.spider import Spider
from bs4 import BeautifulSoup
from datetime import datetime

class SaoneEtLoire(Spider):
    """
    A spider class for crawling the Moselle department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, ouputDir, configFile, linkFile, date):
        """
        Initialize the Moselle spider with specific parameters.
        """
        super().__init__(ouputDir, configFile, linkFile, date)
        self.baseURL = "https://www.saone-et-loire.gouv.fr/Publications/Recueil-des-actes-administratifs"
        self.region = "BourgogneFrancheComte"
        self.department = "SaoneEtLoire"
        self.currentMostRecentRAA = self.mostRecentRAA

    def findPagesAndLinks(self, html):
        """
        Find the number of pages available in the HTML content.

        :param html: HTML content of a page.
        :return: Number of pages found.
        """
        finalLinks = []
        i = 0
        while True:
            links = []
            url = self.baseURL + "/(offset)/" + str(i*10) # Pagination URL the value of offset is multiplied by 10 to get the next page
            
            html = self.fetchPage(url)
            soup = BeautifulSoup(html, 'html.parser')
            i += 1

            if not html or not soup.find(class_="fr-card__title"):
                break

            html = self.fetchPage(url)
            if not html:
                break

            links = self.extractLinks(html, links)
            if len(links) == 0:
                break
            finalLinks.extend(links)
            
        return finalLinks
        
    def extractLinks(self, html, links):
        """
        Extract all links from the HTML content.

        :param html: HTML content of a page.
        :return: List of extracted links.
        """
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('div', class_="fr-card__content")
        for row in rows:
            try:
                dateStr = row.find('p', class_='fr-card__detail').text.split()[-1] # Extract the date from the link text
                date = datetime.strptime(dateStr, "%d/%m/%Y")

                if date > self.mostRecentRAA:           # If the date is more recent than the most recent RAA, add it to the list
                    link = row.find('a', class_='fr-card__link')['href'] # Extract the link from the row
                    links.append({"link": 'https://www.saone-et-loire.gouv.fr' + link, "datePublication": dateStr, "region": self.region, "department": self.department}) # Add the link to the list for JSON output
                    if date > self.currentMostRecentRAA:
                        self.currentMostRecentRAA = date

            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return links
        
    def crawl(self):
        """
        Crawl the website to find and download the most recent RAA links.
        """
        print(f"Starting crawl for {self.department} in {self.region}...")
        try:
            links = self.findPagesAndLinks(self.fetchPage(self.baseURL))

            if self.currentMostRecentRAA > self.mostRecentRAA:  
                self.mostRecentRAA = self.currentMostRecentRAA
                self.setMostRecentRAADate(self.mostRecentRAA, self.region, self.department)

            self.addToJsonResultFile(links)

        except Exception as e:
            print(f"Error during crawling: {e}")
            return None
        
        return self.mostRecentRAA 
    



