import threading
import json
import os
import time
from furet import settings
import ast 

class Crawler:
    """
    A class to manage and execute web crawling tasks using dynamically loaded spiders.
    Attributes:
        configFile (str): Path to the configuration file containing regions and departments data.
        linkFile (str): Path to the file containing links to be used by the spiders.
        spiders (list): A list to store instances of dynamically created spider objects.
    Methods:
        __init__(configFile, linkFile):
            Initializes the Crawler with the given configuration and link files.
        createSpiders(outputDir):
            Dynamically loads and creates spider instances based on the configuration file.
            Spiders are stored in the `spiders` attribute.
        startSpiders():
            Starts all created spiders in separate threads and waits for their completion.
    """
    def __init__(self):
        self.spiders = []
        self.outputDir = os.path.join(os.path.dirname(__file__), "PDFs")

    def createSpiders(self):
        """
        Creates spider instances for each department in the configuration file.
        This method reads the configuration file to retrieve region and department
        information. For each department, it dynamically imports the corresponding
        spider class and creates an instance of it. The created spider instances
        are stored in the `self.spiders` list.
        Raises:
            ImportError: If the module corresponding to a region cannot be imported.
            AttributeError: If the class corresponding to a department cannot be found
                            in the imported module.
        Notes:
            - The configuration file is expected to be in JSON format and should
              contain a "regions" key with nested "departments" data.
            - Module and class names are derived from region and department names
              by removing spaces to ensure valid identifiers.
            - Any errors during the dynamic import or class retrieval are caught
              and logged, but the process continues for other regions and departments.
        """

        config = self.configFile

        for region, regionData in config["regions"].items():
            for department, lastDate in regionData["departments"].items():
                moduleName = region.replace(" ", "").lower().lower() # Remove spaces and convert to lowercase for valid module names
                className = department.replace(" ", "")  # Remove spaces for valid class names
                try:
                    
                    module = __import__(f"furet.crawler.regions.{moduleName}", fromlist=[className])
                    spiderClass = getattr(module, className)
                    listPoc = ["AlpesDeHauteProvence", "Calvados", "BouchesDuRhone", "SaoneEtLoire", "Allier", "Sarthe", "Charente"]
                    if department in listPoc:
                        spider = spiderClass(self.outputDir+f"/{region}/{department}", self.configFile, self.linkFile, lastDate) 
                        self.spiders.append(spider)
                except (ImportError, AttributeError) as e:
                    print(f"Error loading spider for {department} in {region}: {e}")

    def run_spider(self, spider, results):
            start_time = time.time()
            print(f"Starting spider for {spider.department} in {spider.region}...")
            result = spider.crawl()
            end_time = time.time()
            print(f"Spider for {spider.department} in {spider.region} finished in {end_time - start_time:.2f} seconds.")
            results.append(result)
    
    def startSpiders(self):
        """
        Starts the crawling process for all spiders in the `self.spiders` list.
        This method creates a separate thread for each spider's `crawl` method,
        starts all threads, and waits for their completion by joining them.
        Note:
            - Each spider in `self.spiders` is expected to have a `crawl` method.
            - This method blocks until all threads have finished execution.
        """

        threads = []
        results = []
        jsonList = []

        for spider in self.spiders:
            thread = threading.Thread(target=self.run_spider, args=(spider, results))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
        
        for list in results:
            if list is not None:
                jsonList.extend(list)

        return jsonList
    
    def startCrawler(self):
        """
        Starts the crawling process by creating and starting spiders.
        This method is a wrapper around `createSpiders` and `startSpiders`.
        """

        self.configFile = ast.literal_eval(settings.value("crawler.config"))

        linkFile = os.path.join(settings.value("crawler.result"), "resultCrawler.json")
        with open(linkFile, 'w') as f:
            json.dump({"links": []}, f, indent=4)
        self.linkFile = linkFile
        
        self.createSpiders()  
        self.startSpiders()
        print("All spiders have finished crawling.")

