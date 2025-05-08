from furet.crawler.spider import Spider
from bs4 import BeautifulSoup
from datetime import datetime

class Allier(Spider):
    """
    A spider class for crawling the Hautes-Pyrenees department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the HautesPyrenees spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseUrl = "https://www.allier.gouv.fr/Publications/Recueil-des-actes-administratifs-arretes"
        self.region = "AURA"
        self.department = "Allier"
        self.currentMostRecentRAA = self.mostRecentRAA

    def findPages(self, html):
        """
        Find the number of pages available in the HTML content.

        :param html: HTML content of a page.
        :return: Number of pages found.
        """
        extractedPages = []
        soup = BeautifulSoup(html, 'html.parser') 
        
        RAAYear = soup.find_all('h2', class_='fr-card__title')

        for h2 in RAAYear:
            a = h2.find('a', href=True)
            if a['href'].startswith('/Publications/Recueil-des-actes-administratifs-arretes/Recueil-des-actes-administratifs-de-l-annee-'):
                annee = a.text.split()[-1] # Extract the year from the link text
                if int(annee) < self.mostRecentRAA.year: # Check if the year is less than the most recent RAA year for the optimization. We can stop the loop here earlier.
                    break
                extractedPages.append("https://www.allier.gouv.fr" + a['href']) # Add the link to the list of links to be crawled

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
                    links.append({"link": 'https://www.allier.gouv.fr' + link, "datePublication": date_str, "region": self.region, "department": self.department})
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
