from furet.crawler.spider import Spider
from bs4 import BeautifulSoup
from datetime import datetime

class Nord(Spider):
    """
    A spider class for crawling the Nord department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the Nord spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseUrl = "https://www.nord.gouv.fr/Publications/Recueils-des-actes-administratifs/RAA-du-departement-du-Nord/2025"
        self.region = "HautsDeFrance"
        self.department = "Nord"
        self.currentMostRecentRAA = self.mostRecentRAA

    def findPages(self, html):
        """
        Find the number of pages available in the HTML content.

        :param html: HTML content of a page.
        :return: Number of pages found.
        """
        extractedPages = []
        url = self.baseUrl
        html = self.fetchPage(url)
        soup = BeautifulSoup(html, 'html.parser')
        RAAMonths = soup.find_all('a', class_='fr-sidemenu__link')
        for RAAMonth in RAAMonths:
            if RAAMonth['href'].startswith('/Publications/Recueils-des-actes-administratifs/RAA-du-departement-du-Nord'):
                annee = RAAMonth['href'].split('/')[-2]
                if int(annee[-4:]) < self.mostRecentRAA.year: # Check if the year is less than the most recent RAA year for the optimization. We can stop the loop here earlier.
                    break
                        
                extractedPages.append("https://www.nord.gouv.fr" + RAAMonth['href'])
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
                dateStr = row.find('span', class_='fr-link__detail').text.split()[-1] # Extract the date from the title attribute
                date = datetime.strptime(dateStr, "%d/%m/%Y")

                if date > self.mostRecentRAA:
                    link = row['href']
                    links.append({"link": 'https://www.nord.gouv.fr' + link, "datePublication": dateStr, "region": self.region, "department": self.department}) # Add the link to the list for the JSON file
                    if date > self.currentMostRecentRAA:
                        self.currentMostRecentRAA = date

            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return links

    def crawl(self):
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
            print(f"Error during crawling: {e}")
            return None
        
        return links
    
class PasDeCalais(Spider):
    """
    A spider class for crawling the Gers department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the Gers spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseURL = "https://www.pas-de-calais.gouv.fr/Publications/Recueil-des-actes-administratifs"
        self.region = "HautsDeFrance"
        self.department = "PasDeCalais"
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
                if link['href'].startswith('/Publications/Recueil-des-actes-administratifs'):
                    extractedPages.append("https://www.pas-de-calais.gouv.fr" + link['href'])

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
                    links.append({"link": 'https://www.pas-de-calais.gouv.fr' + link, "datePublication": date_str, "region": self.region, "department": self.department})
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

                html = self.fetchPage(link) # The URL for the specific year
                if not html:
                    break

                self.extractLinks(html, links)
            
            if self.currentMostRecentRAA > self.mostRecentRAA:
                self.mostRecentRAA = self.currentMostRecentRAA
                self.setMostRecentRAADate(self.mostRecentRAA, self.region, self.department)

            self.addToJsonResultFile(links)

        except Exception as e:
            print(f"Error during crawling in {self.department}: {e}")
            return None        
        return links