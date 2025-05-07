from spider import Spider
from bs4 import BeautifulSoup
from datetime import datetime
import requests

class Sarthe(Spider):
    def __init__(self, output_dir, configFile, linkFile, date):
        """
        Initialize the Moselle spider with specific parameters.
        """
        super().__init__(output_dir, configFile, linkFile, date)
        self.base_url = "https://www.sarthe.gouv.fr/Publications/Recueils-des-actes-administratifs"
        self.region = "PaysDeLaLoire"
        self.department = "Sarthe"
        self.current_most_recent_RAA = self.most_recent_RAA

    def post_selected_year(self, year):
        """
        Select a specific year by simulating a POST request to refresh the page.

        :param year: The year to select.
        :return: HTML content of the refreshed page.
        """
        headers = {
            "Content-Length": "72",
            "Cache-Control": "max-age=0",
            "Sec-Ch-Ua": "\"Chromium\";v=\"135\", \"Not-A.Brand\";v=\"8\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Accept-Language": "fr-FR,fr;q=0.9",
            "Origin": "https://www.sarthe.gouv.fr",
            "Content-Type": "application/x-www-form-urlencoded",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://www.sarthe.gouv.fr/Publications/Recueils-des-actes-administratifs",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=0, i"
        }
        payload = f"Liste-liste-docs=Publications%2FRecueils-des-actes-administratifs%2F{year}"
        
        response = requests.post(self.base_url, data=payload, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to select year {year}. Status code: {response.status_code}")
            return None
        
    def find_pages(self, html):
        """
        Find the number of pages available in the HTML content.

        :param html: HTML content of a page.
        :return: Number of pages found.
        """
        extracted_pages = []
        soup = BeautifulSoup(html, 'html.parser')         
        RAA_years = soup.find_all('option', value=True, title=True)
        for year in RAA_years:
            year_value = year['title']
            if int(year_value) < self.most_recent_RAA.year: # If the year is older than the most recent RAA, skip it
                break
            html_content = self.post_selected_year(year_value)
            extracted_pages.append(html_content)

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
                    links.append({"link": 'https://www.sarthe.gouv.fr' + link, "datePublication": date_str, "region": self.region, "department": self.department})
                    if date > self.current_most_recent_RAA:
                        self.current_most_recent_RAA = date

            except (ValueError, IndexError) as e:
                print(f"Error parsing row: {row}, Error: {e}")
                continue

        return links
    
        
    def crawl(self):
        try:
            html_pages = self.find_pages(self.fetch_page(self.base_url)) # For each year, there is a page with RAAs
            links = []
            for html_page in html_pages:
            #    if int(link[-4:]) < self.most_recent_RAA.year: # If the year is older than the most recent RAA, skip it
            #       break

                url = self.base_url
                print(f"Crawling: {url}")
                #html = self.fetch_page(url)
                if not html_page:
                    break

                self.extract_links(html_page, links)
            
            # for link in links:
                # self.download_pdf(link)
            
            if self.current_most_recent_RAA > self.most_recent_RAA:
                self.most_recent_RAA = self.current_most_recent_RAA
                self.set_most_recent_RAA_date(self.most_recent_RAA, self.region, self.department)

            self.createJsonResultFile(links)

        except Exception as e:
            print(f"Error during crawling: {e}")
            return None
        
        return self.most_recent_RAA

if __name__ == "__main__":
    spider = Sarthe("./pdfs/")
    spider.crawl()