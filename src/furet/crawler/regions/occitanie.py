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
        self.baseUrl = "https://www.hautes-pyrenees.gouv.fr/Publications/Recueil-d-actes-administratifs"
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
            url = self.baseUrl + "/(offset)/" + str(i*10)  

            html = self.fetchPage(url)
            soup = BeautifulSoup(html, 'html.parser')
            i += 1

            if not html or not soup.find(class_="fr-card__link"):   # Check if the page is empty or if there are no more links to extract
                break
            
            RAA_year = soup.find_all('a', class_='fr-card__link', href=True) # Find all links with the class 'fr-card__link'

            for link in RAA_year:
                if link['href'].startswith('/Publications/Recueil-d-actes-administratifs'):
                    if int(link["href"][-4:]) < self.mostRecentRAA.year: # If the year is older than the most recent RAA, skip it
                        break
                    extractedPages.append("https://www.hautes-pyrenees.gouv.fr" + link['href'])

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

    

class Gers(Spider):
    """
    A spider class for crawling the Gers department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the Gers spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseUrl = "https://www.gers.gouv.fr/Publications/Recueil-des-Actes-Administratifs-RAA"
        self.region = "Occitanie"
        self.department = "Gers"
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
            url = self.baseUrl + "/(offset)/" + str(i*10)  

            html = self.fetchPage(url)
            soup = BeautifulSoup(html, 'html.parser')
            i += 1

            if not html or not soup.find(class_="fr-card__link"):   # Check if the page is empty or if there are no more links to extract
                break
            
            RAA_year = soup.find_all('a', class_='fr-card__link', href=True) # Find all links with the class 'fr-card__link'

            for link in RAA_year:
                if link['href'].startswith('/Publications/Recueil-des-Actes-Administratifs-RAA'):
                    if int(link["href"][-4:]) < self.mostRecentRAA.year: # If the year is older than the most recent RAA, skip it
                        break
                    extractedPages.append("https://www.gers.gouv.fr" + link['href'])

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
                    links.append({"link": 'https://www.gers.gouv.fr' + link, "datePublication": date_str, "region": self.region, "department": self.department})
                    if date > self.currentMostRecentRAA:
                        self.currentMostRecentRAA = date

            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return links

    
class Herault(Spider):
    """
    A spider class for crawling the Herault department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the Herault spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseUrl = "https://www.herault.gouv.fr/Publications/Recueils-des-actes-administratifs"
        self.region = "Occitanie"
        self.department = "Herault"
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
            url = self.baseUrl + "/(offset)/" + str(i*10)  

            html = self.fetchPage(url)
            soup = BeautifulSoup(html, 'html.parser')
            i += 1

            if not html or not soup.find(class_="fr-card__link"):   # Check if the page is empty or if there are no more links to extract
                break
            
            RAA_year = soup.find_all('a', class_='fr-card__link', href=True) # Find all links with the class 'fr-card__link'

            for link in RAA_year:
                if link['href'].startswith('/Publications/Recueils-des-actes-administratifs'):
                    if int(link['href'][-4:]) < self.mostRecentRAA.year: # If the year is older than the most recent RAA, skip it
                        break
                    extractedPages.append("https://www.herault.gouv.fr" + link['href'])

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
                    links.append({"link": 'https://www.herault.gouv.fr' + link, "datePublication": date_str, "region": self.region, "department": self.department})
                    if date > self.currentMostRecentRAA:
                        self.currentMostRecentRAA = date

            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return links

    
class Ariege(Spider):
    """
    A spider class for crawling the Ariege department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the Ariege spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseUrl = "https://www.ariege.gouv.fr/Publications/Recueil-des-actes-administratifs/Recueils-des-Actes-Administratifs-de-l-Ariege-a-partir-du-28-avril-2015"
        self.region = "Occitanie"
        self.department = "Ariege"
        self.currentMostRecentRAA = self.mostRecentRAA

    def findPages(self, html):
        """
        Find the number of pages available in the HTML content.

        :param html: HTML content of a page.
        :return: Number of pages found.
        """
        extractedPages = []
        i = 0
        while True:
            url = self.baseUrl+ "/(offset)/" + str(i*10) # Pagination URL the value of offset is multiplied by 10 to get the next page
            
            html = self.fetchPage(url)
            soup = BeautifulSoup(html, 'html.parser')
            if not html or not soup.find(class_="fr-card__link"):
                break
            i += 1

            RAAYears = soup.find_all('a', class_='fr-card__link')
            for RAAYear in RAAYears:
                if RAAYear['href'].startswith('/Publications/Recueil-des-actes-administratifs/Recueils-des-Actes-Administratifs-de-l-Ariege'):
                    annee = RAAYear['href'].split('-')[-1]
                    if int(annee[-4:]) < self.mostRecentRAA.year: # Check if the year is less than the most recent RAA year for the optimization. We can stop the loop here earlier.
                        break
                            
                    extractedPages.append("https://www.ariege.gouv.fr" + RAAYear['href'])
        return extractedPages

    def extractLinks(self, html, links):
        """
        Extract all links from the HTML content.

        :param html: HTML content of a page.
        :return: List of extracted links.
        """
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('a', href= True)

        for row in rows:
            try:
                if not row['href'].startswith('/contenu/telechargement'):
                    continue
                dateStr = row.find('span', class_='fr-link__detail').text.split()[-1] # Extract the date from the title attribute
                date = datetime.strptime(dateStr, "%d/%m/%Y")

                if date > self.mostRecentRAA:
                    link = row['href']
                    links.append({"link": 'https://www.ariege.gouv.fr' + link, "datePublication": dateStr, "region": self.region, "department": self.department}) # Add the link to the list for the JSON file
                    if date > self.currentMostRecentRAA:
                        self.currentMostRecentRAA = date

            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return links
