from spider import Spider
from bs4 import BeautifulSoup
from datetime import datetime

class AlpesMaritimes(Spider):
    def __init__(self, output_dir, configFile, date):
        """
        Initialize the AlpesMaritimes spider with specific parameters.
        """
        super().__init__(output_dir, configFile, date)
        self.base_url = "https://www.alpes-maritimes.gouv.fr/Publications/Recueil-des-actes-administratifs-RAA"
        self.region = "PACA"
        self.department = "AlpesMaritimes"
        self.current_most_recent_RAA = self.most_recent_RAA

    def find_pages(self, html):
        """
        Find the number of pages available in the HTML content.

        :param html: HTML content of a page.
        :return: Number of pages found.
        """
        extracted_pages = []
        extracted_pages_final = []
        soup = BeautifulSoup(html, 'html.parser')
        
        RAA_year = soup.find_all('h2', class_='fr-card__title')

        for h2 in RAA_year:
            if h2.find('a', href=True)['href'].startswith('/Publications/Recueil-des-actes-administratifs-RAA'):
                annee = h2.find('a', href=True)['href'].split('/')[-1]
                if int(annee[-4:]) < self.most_recent_RAA.year:
                    break

                extracted_pages.append(annee + "/Recueils-mensuels")
                extracted_pages.append(annee + "/Recueils-speciaux")
                extracted_pages.append(annee + "/Recueils-specifiques")

        for link in extracted_pages:
            i = 0
            while True:
                url = self.base_url + '/' + link + "/(offset)/" + str(i*10)
                
                html = self.fetch_page(url)
                soup = BeautifulSoup(html, 'html.parser')
                i += 1

                if not html or not soup.find(class_="fr-card__title"):
                    break

                extracted_pages_final.append(url)

        return extracted_pages_final

    def extract_links(self, html, links):
        """
        Extract all links from the HTML content.

        :param html: HTML content of a page.
        :return: List of extracted links.
        """
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('a', class_="fr-card__link menu-item-link")

        for row in rows:
            try:
                date_str = row["title"].split()[-1]
                date = datetime.strptime(date_str, "%d/%m/%Y")

                if date > self.most_recent_RAA:
                    link = row['href']
                    links.append('https://www.alpes-maritimes.gouv.fr' + link)
                    if date > self.current_most_recent_RAA:
                        self.current_most_recent_RAA = date

            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return links

    def crawl(self):
        try:
            links_pages = self.find_pages(self.fetch_page(self.base_url)) 
            links = []
            for link in links_pages:
                if int(link.split('/')[-4][-4:]) < self.most_recent_RAA.year: 
                    break

                print(f"Crawling: {link}")
                html = self.fetch_page(link)
                if not html:
                    break

                self.extract_links(html, links)

            for link in links:
                self.download_pdf(link)

            if self.current_most_recent_RAA > self.most_recent_RAA:
                self.most_recent_RAA = self.current_most_recent_RAA
                self.set_most_recent_RAA_date(self.most_recent_RAA, self.region, self.department)

        except Exception as e:
            print(f"Error during crawling: {e}")
            return None
        
        return self.most_recent_RAA

if __name__ == "__main__":
    spider = AlpesMaritimes("./pdfs/")
    spider.crawl()