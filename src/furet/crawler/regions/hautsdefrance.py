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
        self.baseUrl = "https://www.nord.gouv.fr/Publications/Recueils-des-actes-administratifs/RAA-du-departement-du-Nord"
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
        extractedPagesFinal = []
        soup = BeautifulSoup(html, 'html.parser') 
        
        h2List = soup.find_all('h2', class_='fr-card__title')

        for h2 in h2List:
            a = h2.find('a', href=True)
            if a['href'].startswith('/Publications/Recueils-des-actes-administratifs/RAA-du-departement-du-Nord'):
                annee = a.text.split()[-1] # Extract the year from the link
                if int(annee) < self.mostRecentRAA.year: # Check if the year is less than the most recent RAA year for the optimization. We can stop the loop here earlier.
                    break
                extractedPages.append('https://www.nord.gouv.fr' + a['href']) 

        for link in extractedPages:
            html = self.fetchPage(link)
            soup = BeautifulSoup(html, 'html.parser')
            h2List2 = soup.find_all('h2', class_='fr-card__title')
            h2List2.reverse() # Reverse the list to get the most recent RAA first
            for h2 in h2List2:
                a2 = h2.find('a', href=True)
                if a2['href'].startswith('/Publications/Recueils-des-actes-administratifs/RAA-du-departement-du-Nord'):
                    month = a2.text.split()[-1] # Extract the year from the link
                    if self.months.get(month.lower()) < self.mostRecentRAA.month: # Check if the month is less than the most recent RAA month for the optimization. We can stop the loop here earlier.
                        break
                    extractedPagesFinal.append('https://www.nord.gouv.fr' + a2['href'])

        return extractedPagesFinal

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
        self.baseUrl = "https://www.pas-de-calais.gouv.fr/Publications/Recueil-des-actes-administratifs"
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
            url = self.baseUrl + "/(offset)/" + str(i*10)  

            html = self.fetchPage(url)
            soup = BeautifulSoup(html, 'html.parser')
            i += 1

            if not html or not soup.find(class_="fr-card__link"):   # Check if the page is empty or if there are no more links to extract
                break
            
            RAA_year = soup.find_all('a', class_='fr-card__link', href=True) # Find all links with the class 'fr-card__link'

            for link in RAA_year:
                if link['href'].startswith('/Publications/Recueil-des-actes-administratifs'):
                    annee = link['href'].split('/')[-1]
                    if int(annee[:4]) < self.mostRecentRAA.year:
                        break
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
    
class Somme(Spider):
    """
    A spider class for crawling the Somme department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the Somme spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseUrl = "https://www.somme.gouv.fr/Publications/Recueil-des-actes-administratifs-du-departement-de-la-Somme"
        self.region = "HautsDeFrance"
        self.department = "Somme"
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

        h2List = soup.find_all('h2', class_='fr-card__title')
        for h2 in h2List:
            a = h2.find('a', href=True)
            if a['href'].startswith('/Publications/Recueil-des-actes-administratifs-du-departement-de-la-Somme/Annee'):
                annee = a['href'].split('-')[-1]
                if int(annee) < self.mostRecentRAA.year:
                    break    
                extractedPages.append( "https://www.somme.gouv.fr" + a['href'])

        return extractedPages
    

    def extractLinks(self, html, links):
        """
        Extract all links from the HTML content.

        :param html: HTML content of a page.
        :return: List of extracted links.
        """
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('a', href= True, class_='fr-link')
        rows.reverse()

        for row in rows:
            try:
                if row['href'].startswith('https://www.somme.gouv.fr/contenu/telechargement') and row.text != "RAA n°61 spécial du 1er avril 2025":
                    a= row.text.split()
                    dateStr = a[-3] + "/" + str(self.months.get(a[-2].lower()))+ "/" + a[-1] # Extract the date from the link text
                    date = datetime.strptime(dateStr, "%d/%m/%Y")

                    if date > self.mostRecentRAA:
                        link = row['href']
                        links.append({"link": link, "datePublication": dateStr, "region": self.region, "department": self.department}) # Add the link to the list for the JSON file
                        if date > self.currentMostRecentRAA:
                            self.currentMostRecentRAA = date

            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return links
