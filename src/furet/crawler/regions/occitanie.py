from furet.crawler.spider import Spider
from bs4 import BeautifulSoup
from datetime import datetime

class HautesPyrenees(Spider):
    """
    A spider class for crawling the Hautes-Pyrenees department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the HautesPyrenees spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseURL = "https://www.hautes-pyrenees.gouv.fr/Publications/Recueil-d-actes-administratifs"
        self.region = "Occitanie"
        self.department = "HautesPyrenees"
        self.currentMostRecentRAA = self.mostRecentRAA

    def findPages(self, html):
        """
        Find the number of pages available in the HTML content.

        :param html: HTML content of a page.
        :return: Number of pages found.
        """
        extractedPages = []
        i = 0
        while True:     # Loop through the pages until there are no more pages to fetch
            url = self.baseURL + "/(offset)/" + str(i*10)  

            html = self.fetchPage(url)
            soup = BeautifulSoup(html, 'html.parser')
            i += 1

            if not html or not soup.find(class_="fr-card__link"):   # Check if the page is empty or if there are no more links to extract
                break
            
            RAA_year = soup.find_all('a', class_='fr-card__link', href=True) # Find all links with the class 'fr-card__link'

            for link in RAA_year:
                if link['href'].startswith('/Publications/Recueil-d-actes-administratifs'):
                    extractedPages.append(link['href'].split('/')[-1])

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
                date_str = row.find('span', class_='fr-link__detail').text.split()[-1] # Extract the date from the link text
                date = datetime.strptime(date_str, "%d/%m/%Y")

                if date > self.mostRecentRAA:            # If the date is more recent than the most recent RAA, add it to the list
                    link = row['href']
                    links.append({"link": 'https://www.hautes-pyrenees.gouv.fr' + link, "datePublication": date_str, "region": self.region, "department": self.department})
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
        try:
            links_suffix = self.findPages(self.fetchPage(self.baseURL)) # For each year, there is a page with RAAs
            links = []
            for link in links_suffix:
                if int(link[-4:]) < self.mostRecentRAA.year: # If the year is older than the most recent RAA, skip it
                    break

                url = self.baseURL + "/" + link # The URL for the specific year
                html = self.fetchPage(url)
                if not html:
                    break

                self.extractLinks(html, links)
            
            if self.currentMostRecentRAA > self.mostRecentRAA:
                self.mostRecentRAA = self.currentMostRecentRAA
                self.setMostRecentRAADate(self.mostRecentRAA, self.region, self.department)

            self.addToJsonResultFile(links)

        except Exception as e:
            print(f"Error during crawling: {e}")
            return None
        
        return self.mostRecentRAA
