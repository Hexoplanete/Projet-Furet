from furet.crawler.spider import Spider
from bs4 import BeautifulSoup
from datetime import datetime


class Moselle(Spider):
    """
    A spider class for crawling the Moselle department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, ouputDir, configFile, linkFile, date):
        """
        Initialize the Moselle spider with specific parameters.
        """
        super().__init__(ouputDir, configFile, linkFile, date)
        self.baseUrl = "https://mc.moselle.gouv.fr/raa.html?adminedit=1?op=raa&do=raa_rec&page="
        self.region = "GrandEst"
        self.department = "Moselle"
        self.currentMostRecentRAA = self.mostRecentRAA
        
    def extractLinks(self, html):
        """
        Extract all links from the HTML content.

        :param html: HTML content of a page.
        :return: List of extracted links.
        """
        soup = BeautifulSoup(html, 'html.parser')
        extractedData = []
        rows = soup.find_all('tr', class_=['li1', 'li2'])

        for row in rows:
            if not "javascript:void(0);" in str(row):
                continue
            try:
                dateStr = row.find_all('td')[2].text.strip() if len(row.find_all('td')) >= 4 else None # Extract the date from the row
                if not dateStr:
                    continue
                date = datetime.strptime(dateStr, "%d/%m/%Y")

                linkTag = row.find_all('a', href=True)[1] if len(row.find_all('td')) >= 2 else None     # Extract the link from the row
                if not linkTag:
                    continue

                if date > self.mostRecentRAA:             # If the date is more recent than the most recent RAA, add it to the list
                    link = linkTag['href']
                    extractedData.append({"link": link, "datePublication": dateStr, "region": self.region, "department": self.department})
                    if date > self.currentMostRecentRAA:
                        self.currentMostRecentRAA = date
            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return extractedData
        
    def crawl(self):
        """
        Crawl the website to find and download the most recent RAA links.
        Moselle's website has a specific pagination structure, so we need to handle that.
        """
        try:
            i = 1
            finalLinks = []
            while True:           # Loop through the pages until no more links are found
                url = self.baseUrl + str(i)
                i += 1
                html = self.fetchPage(url)
                if not html or "Il n'y a aucun recueil cr" in html: # Check if the page is empty or if there are no more RAA
                    break

                links = self.extractLinks(html)
                if links == []:     # if no more links are found, break the loop because every subsequent RAA will be too old
                    break

                for link in links:
                    finalLinks.append(link)
            
            if self.currentMostRecentRAA > self.mostRecentRAA:  
                self.mostRecentRAA = self.currentMostRecentRAA
                self.setMostRecentRAADate(self.mostRecentRAA, self.region, self.department)

            self.addToJsonResultFile(finalLinks)

        except Exception as e:
            print(f"Error during crawling in {self.department}: {e}")
            return None
        
        return finalLinks
    

class Aube(Spider):
    """
    A spider class for crawling the Ariege department's website for RAA (Recueil des Actes Administratifs) links.
    Inherits from the Spider class.
    """
    def __init__(self, outputDir, configFile, linkFile, date):
        """
        Initialize the Ariege spider with specific parameters.
        """
        super().__init__(outputDir, configFile, linkFile, date)
        self.baseUrl = "https://www.aube.gouv.fr/Publications/RAA-Recueil-des-Actes-Administratifs"
        self.region = "GrandEst"
        self.department = "Aube"
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
        
        div = soup.find('div', class_='fr-text--lead fr-my-3w')
        aList = div.find_all('a', href=True, class_='fr-link')

        for a in aList:
            if a['href'].startswith('/Publications/RAA-Recueil-des-Actes-Administratifs/RAA'):
                annee = a.text.split()[-1] # Extract the year from the link
                if int(annee) < self.mostRecentRAA.year: # Check if the year is less than the most recent RAA year for the optimization. We can stop the loop here earlier.
                    continue
                extractedPages.append('https://www.aube.gouv.fr' + a['href']) 

        for link in extractedPages:
            i = 0
            while True:
                url = link + "/(offset)/" + str(i*10) # Pagination URL the value of offset is multiplied by 10 to get the next page
                
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
        rows = soup.find_all('a', href=True, class_='fr-card__link menu-item-link')

        for row in rows:
            try:
                if not row['href'].startswith('/contenu/telechargement'):
                    continue
                dateStr = row["title"].split()[-1] # Extract the date from the title attribute
                date = datetime.strptime(dateStr, "%d/%m/%Y")

                if date > self.mostRecentRAA:
                    link = row['href']
                    links.append({"link": 'https://www.aube.gouv.fr' + link, "datePublication": dateStr, "region": self.region, "department": self.department}) # Add the link to the list for the JSON file
                    if date > self.currentMostRecentRAA:
                        self.currentMostRecentRAA = date

            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return links


    
