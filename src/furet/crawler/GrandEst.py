from spider import Spider
from bs4 import BeautifulSoup
from datetime import datetime
import os
import requests

class Moselle(Spider):
    def __init__(self, output_dir, configFile, linkFile, date):
        """
        Initialize the Moselle spider with specific parameters.
        """
        super().__init__(output_dir, configFile, linkFile, date)
        self.base_url = "https://mc.moselle.gouv.fr/raa.html?adminedit=1?op=raa&do=raa_rec&page="
        self.region = "GrandEst"
        self.department = "Moselle"
        self.current_most_recent_RAA = self.most_recent_RAA
        
    def extract_links(self, html):
        """
        Extract all links from the HTML content.

        :param html: HTML content of a page.
        :return: List of extracted links.
        """
        soup = BeautifulSoup(html, 'html.parser')
        extracted_data = []
        rows = soup.find_all('tr', class_=['li1', 'li2'])

        for row in rows:
            if not "javascript:void(0);" in str(row):
                continue
            try:
                date_str = row.find_all('td')[2].text.strip() if len(row.find_all('td')) >= 4 else None
                if not date_str:
                    continue
                date = datetime.strptime(date_str, "%d/%m/%Y")

                link_tag = row.find_all('a', href=True)[1] if len(row.find_all('td')) >= 2 else None
                if not link_tag:
                    continue

                if date > self.most_recent_RAA:
                    link = link_tag['href']
                    extracted_data.append({"link": link, "datePublication": date_str, "region": self.region, "department": self.department})
                    if date > self.current_most_recent_RAA:
                        self.current_most_recent_RAA = date
            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return extracted_data
    
    def download_pdf(self, url):
        """
        Download a PDF file from the given URL.

        :param url: URL of the PDF file.
        """
        try:
            response = requests.get(url, stream=True, headers=self.headers)
            response.raise_for_status()
            
            filename = os.path.join(self.output_dir, url[-10:])
            if not filename.endswith('.pdf'):
                filename += ".pdf"
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Downloaded: {filename}")
        except requests.RequestException as e:
            print(f"Failed to download {url}: {e}")
        
    def crawl(self):
        try:
            i = 1
            finalLinks = []
            while True:
                url = self.base_url + str(i)
                i += 1
                print(f"Crawling: {url}")
                html = self.fetch_page(url)
                if not html or "Il n'y a aucun recueil cr" in html:
                    break

                links = self.extract_links(html)
                if links == []:     # if no more links are found, break the loop because every subsequent RAA will be too old
                    break

                for link in links:
                    # self.download_pdf(link)
                    finalLinks.append(link)

            
            if self.current_most_recent_RAA > self.most_recent_RAA:
                self.most_recent_RAA = self.current_most_recent_RAA
                self.set_most_recent_RAA_date(self.most_recent_RAA, self.region, self.department)

            self.createJsonResultFile(finalLinks)

        except Exception as e:
            print(f"Error during crawling: {e}")
            return None
        
        return self.most_recent_RAA 

if __name__ == "__main__":
    spider = Moselle("./pdfs/")
    spider.crawl()