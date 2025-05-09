from furet.crawler.spider import Spider
from bs4 import BeautifulSoup
from datetime import datetime

class Charente(Spider):
    """
    A spider class for crawling the Charente department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the Ariege spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseUrl = "https://www.charente.gouv.fr/Publications/Recueil-des-actes-administratifs2"
        self.region = "NouvelleAquitaine"
        self.department = "Charente"
        self.currentMostRecentRAA = self.mostRecentRAA

    def findPages(self, html):
        """
        Find the number of pages available in the HTML content.

        :param html: HTML content of a page.
        :return: Number of pages found.
        """
        extractedPages = []
        extractedPagesFinal = []
        soup = BeautifulSoup(html, 'html.parser') 
        
        h2List = soup.find_all('h2', class_='fr-card__title')

        for h2 in h2List:
            a = h2.find('a', href=True)
            if a['href'].startswith('/Publications/Recueil-des-actes-administratifs2/Annee-'):
                annee = a.text.split()[-1] # Extract the year from the link
                if int(annee) < self.mostRecentRAA.year: # Check if the year is less than the most recent RAA year for the optimization. We can stop the loop here earlier.
                    break
                extractedPages.append('https://www.charente.gouv.fr' + a['href']) 

        for link in extractedPages:
            html = self.fetchPage(link)
            soup = BeautifulSoup(html, 'html.parser')
            div = soup.find('div', class_='fr-text--lead fr-my-3w')
            aList = div.find_all('a', href=True, class_='fr-link')
            for a in aList:
                if self.months.get(a.text.split()[-2].lower()) >= self.mostRecentRAA.month: # Check if the month is less than the most recent RAA month for the optimization. We can stop the loop here earlier.
                    extractedPagesFinal.append('https://www.charente.gouv.fr' + a['href'])

        return extractedPagesFinal

    def extractLinks(self, html, links):
        """
        Extract all links from the HTML content.

        :param html: HTML content of a page.
        :return: List of extracted links.
        """
        soup = BeautifulSoup(html, 'html.parser')
        a = soup.find('a', href=True, class_='fr-link fr-link--download')

        try:
            dateStr = a.find('span', class_='fr-link__detail').text.split()[-1] # Extract the date from the link
            date = datetime.strptime(dateStr, "%d/%m/%Y")

            if date > self.mostRecentRAA:
                link = a['href']
                links.append({"link": 'https://www.charente.gouv.fr' + link, "datePublication": dateStr, "region": self.region, "department": self.department}) # Add the link to the list for the JSON file
                if date > self.currentMostRecentRAA:
                    self.currentMostRecentRAA = date

        except (ValueError, IndexError) as e:
            print(f"Error parsing row: {a}, Error: {e}")
            return None

        return links


    