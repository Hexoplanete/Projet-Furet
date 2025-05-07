import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import json

class Spider:
    def __init__(self, output_dir, configFile="./config_crawler.json", linkFile="./resultCrawler.json", date="01/01/2025"):
        """
        Initialize the Spider.

        :param base_url: The starting URL for the crawler.
        :param output_dir: Directory to save downloaded PDF files.
        :param link_rules: A list of rules (functions) to filter links.
        """
        self.output_dir = output_dir
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "fr-FR,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }
        self.most_recent_RAA = datetime.strptime(date, "%d/%m/%Y")
        self.configFile = configFile
        self.linkFile = linkFile

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    # def get_most_recent_RAA_date(self, configFile, region, department):
    #     """
    #     Get the most recent RAA date from the configuration file.

    #     :param configFile: Path to the configuration file.
    #     :param date: Date to compare with.
    #     :return: Most recent RAA date.
    #     """
    #     try:
    #         with open(configFile, 'r') as file:
    #             data = json.load(file)
    #             date_str = data.get("regions", {}).get(region, {}).get("departments", {}).get(department, self.defaultDate)
    #             return datetime.strptime(date_str, "%d/%m/%Y")
    #     except (FileNotFoundError, json.JSONDecodeError) as e:
    #         print(f"Error reading config file: {e}")
    #         return datetime.strptime(self.defaultDate, "%d/%m/%Y")
    
    def set_most_recent_RAA_date(self, date, region, department):
        """
        Set the most recent RAA date in the configuration file.

        :param configFile: Path to the configuration file.
        :param date: Date to set.
        """
        try:
            with open(self.configFile, 'r') as file:
                data = json.load(file)
                data["regions"][region]["departments"][department] = date.strftime("%d/%m/%Y")
            
            with open(self.configFile, 'w') as file:
                json.dump(data, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error writing to config file: {e}")

    def fetch_page(self, url):
        """
        Fetch the content of a webpage with headers mimicking a browser.

        :param url: URL of the webpage to fetch.
        :return: HTML content of the page.
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            return None

    def download_pdf(self, url):
        """
        Download a PDF file from the given URL.

        :param url: URL of the PDF file.
        """
        try:
            response = requests.get(url, stream=True, headers=self.headers)
            response.raise_for_status()
            
            filename = os.path.join(self.output_dir, url.split('/')[-1])
            if not filename.endswith('.pdf'):
                filename += ".pdf"
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Downloaded: {filename}")
        except requests.RequestException as e:
            print(f"Failed to download {url}: {e}")

    def createJsonResultFile(self, linkList):
        with open(self.linkFile, "r") as f:
            data = json.load(f)
            data["links"].extend(linkList)
        with open(self.linkFile, "w") as f:
            json.dump(data, f, indent=4) 
        


if __name__ == "__main__":
    spider = Spider(
        base_url="https://mc.moselle.gouv.fr/raa.html?adminedit=1?op=raa&do=raa_rec&page=0",
        output_dir="./pdfs/"
    )
    html = spider.fetch_page(spider.base_url)
    links = spider.extract_links(html)
    print(links)