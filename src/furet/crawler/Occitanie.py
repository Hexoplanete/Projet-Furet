from spider import Spider
from bs4 import BeautifulSoup
from datetime import datetime

class HautesPyrenees(Spider):
    def __init__(self, output_dir, configFile, date):
        """
        Initialize the HautesPyrenees spider with specific parameters.
        """
        super().__init__(output_dir, configFile, date)
        self.base_url = "https://www.hautes-pyrenees.gouv.fr/Publications/Recueil-d-actes-administratifs"
        self.region = "Occitanie"
        self.department = "HautesPyrenees"
        self.current_most_recent_RAA = self.most_recent_RAA

    def find_pages(self, html):
        """
        Find the number of pages available in the HTML content.

        :param html: HTML content of a page.
        :return: Number of pages found.
        """
        extracted_pages = []
        i = 0
        while True:
            url = self.base_url + "/(offset)/" + str(i*10)
            print(f"Crawling: {url}")

            html = self.fetch_page(url)
            soup = BeautifulSoup(html, 'html.parser')
            i += 1

            if not html or not soup.find(class_="fr-card__link"):
                break
            
            RAA_year = soup.find_all('a', class_='fr-card__link', href=True)

            for link in RAA_year:
                if link['href'].startswith('/Publications/Recueil-d-actes-administratifs'):
                    extracted_pages.append(link['href'].split('/')[-1])

        return extracted_pages

    def extract_links(self, html, links):
        """
        Extract all links from the HTML content.

        :param html: HTML content of a page.
        :return: List of extracted links.
        """
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('a', class_="fr-link fr-link--download")

        for row in rows:
            try:
                date_str = row.find('span', class_='fr-link__detail').text.split()[-1]
                date = datetime.strptime(date_str, "%d/%m/%Y")

                if date > self.most_recent_RAA:
                    link = row['href']
                    links.append('https://www.hautes-pyrenees.gouv.fr' + link)
                    if date > self.current_most_recent_RAA:
                        self.current_most_recent_RAA = date

            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return links

    def crawl(self):
        try:
            links_suffix = self.find_pages(self.fetch_page(self.base_url)) # For each year, there is a page with RAAs
            links = []
            for link in links_suffix:
                if int(link[-4:]) < self.most_recent_RAA.year: # If the year is older than the most recent RAA, skip it
                    break

                url = self.base_url + "/" + link
                print(f"Crawling: {url}")
                html = self.fetch_page(url)
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
    spider = HautesPyrenees("./pdfs/")
    spider.crawl()