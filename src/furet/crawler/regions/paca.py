from furet.crawler.spider import Spider
from bs4 import BeautifulSoup
from datetime import datetime

class AlpesMaritimes(Spider):
    """
    A spider class for crawling the Alpes-Maritimes department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the AlpesMaritimes spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseUrl = "https://www.alpes-maritimes.gouv.fr/Publications/Recueil-des-actes-administratifs-RAA"
        self.region = "PACA"
        self.department = "AlpesMaritimes"
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
        
        RAAYear = soup.find_all('h2', class_='fr-card__title')

        for h2 in RAAYear:
            if h2.find('a', href=True)['href'].startswith('/Publications/Recueil-des-actes-administratifs-RAA'):
                annee = h2.find('a', href=True)['href'].split('/')[-1]
                if int(annee[-4:]) < self.mostRecentRAA.year: # Check if the year is less than the most recent RAA year for the optimization. We can stop the loop here earlier.
                    break

                extractedPages.append(annee + "/Recueils-mensuels")
                extractedPages.append(annee + "/Recueils-speciaux")
                extractedPages.append(annee + "/Recueils-specifiques")

        for link in extractedPages:
            i = 0
            while True:
                url = self.baseUrl + '/' + link + "/(offset)/" + str(i*10) # Pagination URL the value of offset is multiplied by 10 to get the next page
                
                html = self.fetchPage(url)
                soup = BeautifulSoup(html, 'html.parser')
                i += 1

                if not html or not soup.find(class_="fr-card__title"):
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
        rows = soup.find_all('a', class_="fr-card__link menu-item-link")

        for row in rows:
            try:
                dateStr = row["title"].split()[-1] # Extract the date from the title attribute
                date = datetime.strptime(dateStr, "%d/%m/%Y")

                if date > self.mostRecentRAA:
                    link = row['href']
                    links.append({"link": 'https://www.alpes-maritimes.gouv.fr' + link, "datePublication": dateStr, "region": self.region, "department": self.department}) # Add the link to the list for the JSON file
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
                # Check if the year is less than the most recent RAA year for the optimization. We can stop the loop here earlier.
                if int(link.split('/')[-4][-4:]) < self.mostRecentRAA.year: 
                    break

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

class BouchesDuRhone(Spider):
    """
    A spider class for crawling the Alpes-Maritimes department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the AlpesMaritimes spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseUrl = "https://www.bouches-du-rhone.gouv.fr/Publications/RAA-et-Archives"
        self.region = "PACA"
        self.department = "BouchesDuRhone"
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
        
        RAAYear = soup.find_all('h2', class_='fr-card__title')

        for h2 in RAAYear:
            a = h2.find('a', href=True)
            if a['href'].startswith('/Publications/RAA-et-Archives/RAA-'):
                annee = h2.find('a', href=True).text.split()[-1]
                if int(annee) < self.mostRecentRAA.year: # Check if the year is less than the most recent RAA year for the optimization. We can stop the loop here earlier.
                    break
                extractedPagesFinal.append("https://www.bouches-du-rhone.gouv.fr" + a['href'])
            elif a['href'].startswith('/Publications/RAA-et-Archives/Archives-RAA-des-Bouches-du-Rhone') and self.mostRecentRAA.year < 2023:
                annee = h2.find('a', href=True).text.split()[-1]
                extractedPages.append("https://www.bouches-du-rhone.gouv.fr" + a['href'])

        for link in extractedPages:
            html = self.fetchPage(self.baseUrl)
            soup = BeautifulSoup(html, 'html.parser') 
            RAAYear = soup.find_all('h2', class_='fr-card__title')
            for h2 in RAAYear:
                if h2.find('a', href=True)['href'].startswith('/Publications/RAA-et-Archives/Archives-RAA-des-Bouches-du-Rhone/RAA-'):
                    annee = h2.find('a', href=True).text.split()[-1]
                    if int(annee) < self.mostRecentRAA.year: # Check if the year is less than the most recent RAA year for the optimization. We can stop the loop here earlier.
                        break
                    extractedPagesFinal.append(h2.find('a', href=True)['href'])

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
                    links.append({"link": 'https://www.bouches-du-rhone.gouv.fr' + link, "datePublication": dateStr, "region": self.region, "department": self.department}) # Add the link to the list for the JSON file
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

class Var(Spider):
    """
    A spider class for crawling the Alpes-Maritimes department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the AlpesMaritimes spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseUrl = "https://www.var.gouv.fr/Publications/RAA-Recueil-des-actes-administratifs/Recueil-des-actes-administratifs-2011"
        self.region = "PACA"
        self.department = "Var"
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
        
        RAAYears = soup.find_all('a', class_='fr-sidemenu__link')

        for RAAYear in RAAYears:
            if RAAYear['href'].startswith('/Publications/RAA-Recueil-des-actes-administratifs'):
                annee = RAAYear['href'].split('-')[-1]
                if int(annee[-4:]) < self.mostRecentRAA.year: # Check if the year is less than the most recent RAA year for the optimization. We can stop the loop here earlier.
                    break
                        
                extractedPages.append(RAAYear['href'])

        for link in extractedPages:
            i = 0
            while True:
                url = "https://www.var.gouv.fr/" + link + "/(offset)/" + str(i*10) # Pagination URL the value of offset is multiplied by 10 to get the next page
                
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
        rows = soup.find_all('a', class_="fr-card__link menu-item-link")

        for row in rows:
            try:
                dateStr = row["title"].split()[-1] # Extract the date from the title attribute
                date = datetime.strptime(dateStr, "%d/%m/%Y")

                if date > self.mostRecentRAA:
                    link = row['href']
                    links.append({"link": 'https://www.var.gouv.fr' + link, "datePublication": dateStr, "region": self.region, "department": self.department}) # Add the link to the list for the JSON file
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

