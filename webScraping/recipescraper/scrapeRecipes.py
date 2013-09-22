from scrapy import project, signals
from scrapy.settings import Settings
<<<<<<< HEAD
from scrapy import log, signals, project
from recipescraper.spiders.recipe_spider import Recipe_Spider
=======
from scrapy.crawler import CrawlerProcess
>>>>>>> 80bdbe0fc08c301a242d40555125e5fbc6398d57
from scrapy.xlib.pydispatch import dispatcher
from multiprocessing.queues import Queue
from recipescraper.spiders.recipe_spider import RecipeSpider
import multiprocessing
 
class CrawlerWorker(multiprocessing.Process):
 
    def __init__(self, result_queue, url):
        multiprocessing.Process.__init__(self)
        self.result_queue = result_queue
        self.url=url
 
        self.crawler = CrawlerProcess(Settings)
        #if not hasattr(project, 'crawler'):
         #   self.crawler.install()
        self.crawler.configure()
 
        self.items = []
        self.spider = RecipeSpider(url)
        dispatcher.connect(self._item_passed, signals.item_passed)
 
    def _item_passed(self, item):
        self.items.append(item)
  
    def run(self):
        self.crawler.crawl(self.spider)
        self.crawler.start()
        self.crawler.stop()
        self.result_queue.put(self.items)

def returnQueue():
  result=Queue()
  crawler=CrawlerWorker(result,"http://allrecipes.com/Recipe/Apple-Pie-2/")
  crawler.run()
  for item in result.get():
    print("a")

returnQueue()
