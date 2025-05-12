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
        self.baseUrl = "https://www.saone-et-loire.gouv.fr/Publications/Recueil-des-actes-administratifs"
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
            url = self.baseUrl + "/(offset)/" + str(i*10) # Pagination URL the value of offset is multiplied by 10 to get the next page
            
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
        SaoneEtLoire department's specific implementation is necessary to handle pagination and link extraction.
        """
        try:
            links = self.findPagesAndLinks(self.fetchPage(self.baseUrl))

            if self.currentMostRecentRAA > self.mostRecentRAA:  
                self.mostRecentRAA = self.currentMostRecentRAA
                self.setMostRecentRAADate(self.mostRecentRAA, self.region, self.department)

            self.addToJsonResultFile(links)

        except Exception as e:
            print(f"Error during crawling in {self.department}: {e}")
            return None
        
        return links
    
class Doubs(Spider):
    """
    A spider class for crawling the Doubs department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the Doubs spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseUrl = "https://www.doubs.gouv.fr/Publications/Publications-Legales/Recueil-des-Actes-Administratifs-RAA"
        self.region = "BourgogneFrancheComte"
        self.department = "Doubs"
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
                if RAAYear['href'].startswith('/Publications/Publications-Legales/Recueil-des-Actes-Administratifs-RAA/Recueil-des-actes-administratifs-pour-le-Doubs'):
                    annee = RAAYear['href'].split('-')[-1]
                    if int(annee[-4:]) < self.mostRecentRAA.year: # Check if the year is less than the most recent RAA year for the optimization. We can stop the loop here earlier.
                        break
                            
                    extractedPages.append("https://www.doubs.gouv.fr" + RAAYear['href'])
        return extractedPages

    def extractLinks(self, html, links):
        """
        Extract all links from the HTML content.

        :param html: HTML content of a page.
        :return: List of extracted links.
        """
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('a', href= True, class_="fr-link fr-link--download")

        for row in rows:
            try:
                dateStr = row.find('span', class_='fr-link__detail').text.split()[-1] # Extract the date from the title attribute
                date = datetime.strptime(dateStr, "%d/%m/%Y")

                if date > self.mostRecentRAA:
                    link = row['href']
                    links.append({"link": 'https://www.doubs.gouv.fr' + link, "datePublication": dateStr, "region": self.region, "department": self.department}) # Add the link to the list for the JSON file
                    if date > self.currentMostRecentRAA:
                        self.currentMostRecentRAA = date

            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return links

class Jura(Spider):
    """
    A spider class for crawling the Jura department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the jura spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseUrl = "https://www.jura.gouv.fr/Publications/Publications-legales/Recueil-des-Actes-Administratifs"
        self.region = "BourgogneFrancheComte"
        self.department = "Jura"
        self.currentMostRecentRAA = self.mostRecentRAA

    def findPages(self, html):
        """
        Find the number of pages available in the HTML content.

        :param html: HTML content of a page.
        :return: Number of pages found.
        """
        extractedPages = []
        extractedPagesFinal = []
        url = self.baseUrl
        
        html = self.fetchPage(url)
        soup = BeautifulSoup(html, 'html.parser')

        h2List = soup.find_all('h2', class_='fr-card__title')
        for h2 in h2List:
            a = h2.find('a', href=True)
            if a['href'].startswith('/Publications/Publications-legales/Recueil-des-Actes-Administratifs/Annee'):
                annee = a['href'].split('-')[-1]
                if int(annee) < self.mostRecentRAA.year:
                    break    
                extractedPages.append(a['href'])


        for link in extractedPages:
            i = 0
            while True:
                url = "https://www.jura.gouv.fr" + link + "/(offset)/" + str(i*10) # Pagination URL the value of offset is multiplied by 10 to get the next page
                
                html = self.fetchPage(url)
                soup = BeautifulSoup(html, 'html.parser')
                i += 1

                if not html or not soup.find(class_="fr-card__link menu-item-link"):
                    break

                extractedPagesFinal.append(url)

        return extractedPagesFinal
    

    def extractLinks(self, html, links):
        """
        Extract all links from the HTML content.

        :param html: HTML content of a page.
        :return: List of extracted links.
        """
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('a', href= True, class_='fr-card__link menu-item-link')

        for row in rows:
            try:
                dateStr = row["title"].split()[-1] # Extract the date from the title attribute
                date = datetime.strptime(dateStr, "%d/%m/%Y")

                if date > self.mostRecentRAA:
                    link = row['href']
                    links.append({"link": 'https://www.jura.gouv.fr' + link, "datePublication": dateStr, "region": self.region, "department": self.department}) # Add the link to the list for the JSON file
                    if date > self.currentMostRecentRAA:
                        self.currentMostRecentRAA = date

            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return links
