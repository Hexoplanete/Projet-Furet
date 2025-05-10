from furet.crawler.spider import Spider
from bs4 import BeautifulSoup
from datetime import datetime


class Loiret(Spider):
    """
    A spider class for crawling the Loiret department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the Loiret spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseUrl = "https://www.loiret.gouv.fr/Publications/Recueil-des-actes-administratifs/Recueil-des-actes-administratifs-departementaux"
        self.region = "CentreValDeLoire"
        self.department = "Loiret"
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
            if a['href'].startswith('/Publications/Recueil-des-actes-administratifs/Recueil-des-actes-administratifs-departementaux/20'):
                annee = a['href'].split('/')[-1]
                if int(annee) < self.mostRecentRAA.year or self.months.get(a.text.split()[-2].lower()) < self.mostRecentRAA.month: # Check if the year is less than the most recent RAA year for the optimization. We can stop the loop here earlier.
                    break    
                extractedPages.append(a['href'])
            else:
                if not a['href'].startswith('/Publications/Recueil-des-actes-administratifs/Recueil-des-actes-administratifs-departementaux/Delegations'):
                    annee = a.text.split()[-1]
                    if int(annee) < self.mostRecentRAA.year:
                        break
                    extractedPagesFinal.append("https://www.loiret.gouv.fr" + a['href'])
            


        for link in extractedPages:
                url = "https://www.loiret.gouv.fr" + link       
                html = self.fetchPage(url)
                soup = BeautifulSoup(html, 'html.parser')

                h2List = soup.find_all('h2', class_='fr-card__title')
                for h2 in h2List:
                    a = h2.find('a', href=True)
                    if a['href'].startswith(link):
                        if self.months.get(a.text.split()[-2].lower()) < self.mostRecentRAA.month:
                            break    
                        extractedPagesFinal.append("https://www.loiret.gouv.fr" + a['href'])

        return extractedPagesFinal
    

    def extractLinks(self, html, links):
        """
        Extract all links from the HTML content.

        :param html: HTML content of a page.
        :return: List of extracted links.
        """
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('a', href= True, class_='fr-link fr-link--download')

        for row in rows:
            try:
                dateStr = row.find('span').text.split()[-1] # Extract the date from the title attribute
                date = datetime.strptime(dateStr, "%d/%m/%Y")

                if date > self.mostRecentRAA:
                    link = row['href']
                    links.append({"link": 'https://www.loiret.gouv.fr' + link, "datePublication": dateStr, "region": self.region, "department": self.department}) # Add the link to the list for the JSON file
                    if date > self.currentMostRecentRAA:
                        self.currentMostRecentRAA = date

            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return links
    
class Indre(Spider):
    """
    A spider class for crawling the Indre department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the Indre spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseUrl = "https://www.indre.gouv.fr/Publications/Recueil-des-actes-administratifs"
        self.region = "CentreValDeLoire"
        self.department = "Indre"
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
            if a['href'].startswith('/Publications/Recueil-des-actes-administratifs/20'):
                annee = a['href'].split('/')[-1]
                if int(annee) < self.mostRecentRAA.year:
                    break    
                extractedPages.append(a['href'])


        for link in extractedPages:
            i = 0
            while True:
                url = "https://www.indre.gouv.fr" + link + "/(offset)/" + str(i*10) # Pagination URL the value of offset is multiplied by 10 to get the next page
                
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
                    links.append({"link": 'https://www.indre.gouv.fr' + link, "datePublication": dateStr, "region": self.region, "department": self.department}) # Add the link to the list for the JSON file
                    if date > self.currentMostRecentRAA:
                        self.currentMostRecentRAA = date

            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return links
    
class Cher(Spider):
    """
    A spider class for crawling the Cher department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the Cher spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseUrl = "https://www.cher.gouv.fr/Publications/Recueil-des-actes-administratifs-RAA-Arretes-et-circulaires/Recueil-des-actes-administratifs"
        self.region = "CentreValDeLoire"
        self.department = "Cher"
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
            if a['href'].startswith('/Publications/Recueil-des-actes-administratifs-RAA-Arretes-et-circulaires/Recueil-des-actes-administratifs/20'):
                annee = a['href'].split('/')[-1]
                if int(annee) < self.mostRecentRAA.year:
                    break    
                extractedPages.append(a['href'])



        for link in extractedPages:
                url = "https://www.cher.gouv.fr" + link       
                html = self.fetchPage(url)
                soup = BeautifulSoup(html, 'html.parser')

                h2List = soup.find_all('h2', class_='fr-card__title')
                h2List.reverse()  # Reverse the list to get the most recent first
                for h2 in h2List:
                    a = h2.find('a', href=True)
                    if a['href'].startswith(link):  
                        if self.months.get(a['href'].split('/')[-1].lower()) < self.mostRecentRAA.month:
                            break
                        extractedPagesFinal.append("https://www.cher.gouv.fr" + a['href'])

        return extractedPagesFinal
    

    def extractLinks(self, html, links):
        """
        Extract all links from the HTML content.

        :param html: HTML content of a page.
        :return: List of extracted links.
        """
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('a', href= True, class_='fr-link fr-link--download')

        for row in rows:
            try:
                dateStr = row["title"].split()[-1] # Extract the date from the title attribute
                date = datetime.strptime(dateStr, "%d/%m/%Y")

                if date > self.mostRecentRAA:
                    link = row['href']
                    links.append({"link": 'https://www.cher.gouv.fr' + link, "datePublication": dateStr, "region": self.region, "department": self.department}) # Add the link to the list for the JSON file
                    if date > self.currentMostRecentRAA:
                        self.currentMostRecentRAA = date

            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return links