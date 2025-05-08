from furet.crawler.spider import Spider
from bs4 import BeautifulSoup
from datetime import datetime

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
        self.baseUrl = "https://www.var.gouv.fr/Publications/RAA-Recueil-des-actes-administratifs"
        self.region = "CoteDAzur"
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
            if RAAYear['href'].startswith('/Publications/Recueil-des-actes-administratifs-RAA'):
                annee = RAAYear['href'].split('-')[-1]
                if int(annee[-4:]) < self.mostRecentRAA.year: # Check if the year is less than the most recent RAA year for the optimization. We can stop the loop here earlier.
                    break
                url = self.baseUrl + '-' + annee
                html = self.fetchPage(url)
                soup = BeautifulSoup(html, 'html.parser')

                RAAmonths = soup.find_all('a', class_='fr-sidemenu__link')
                for RAAmonth in RAAmonths:
                    if RAAmonth['href'].startswith('/Publications/Recueil-des-actes-administratifs-RAA'):
                        month = RAAmonth['href'].split('-')[-2]
                        
                    extractedPages.append(annee + "/" + month + "-" + annee)

        for link in extractedPages:
            i = 0
            while True:
                url = self.baseUrl + '-' + link + "/(offset)/" + str(i*10) # Pagination URL the value of offset is multiplied by 10 to get the next page
                
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
        
        return self.mostRecentRAA
