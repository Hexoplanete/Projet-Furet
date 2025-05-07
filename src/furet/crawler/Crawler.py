import threading
import json
import os

class Crawler:
    def __init__(self, config_file, linkFile):
        self.config_file = config_file
        self.linkFile = linkFile
        self.spiders = []

    def create_spiders(self, output_dir):
        with open(self.config_file, 'r') as file:
            config = json.load(file)

        for region, region_data in config["regions"].items():
            for department, last_date in region_data["departments"].items():
                module_name = region.replace(" ", "")  # Remove spaces for valid module names
                class_name = department.replace(" ", "")  # Remove spaces for valid class names
                try:
                    module = __import__(f"{module_name}", fromlist=[class_name])
                    spider_class = getattr(module, class_name)
                    spider = spider_class(output_dir+f"/{region}/{department}", self.config_file, self.linkFile, last_date)
                    self.spiders.append(spider)
                except (ImportError, AttributeError) as e:
                    print(f"Error loading spider for {department} in {region}: {e}")

    def start_spiders(self):
        threads = []
        for spider in self.spiders:
            thread = threading.Thread(target=spider.crawl)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    # Use an absolute path to ensure the file is found
    config_file = os.path.join(os.path.dirname(__file__), "config_crawler.json")
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file}")
    
    linkFile = os.path.join(os.path.dirname(__file__), "resultCrawler.json")
    if not os.path.exists(linkFile):
        raise FileNotFoundError(f"Link file not found: {linkFile}")

    crawler = Crawler(config_file, linkFile)
    crawler.create_spiders("./pdfs")  
    crawler.start_spiders()