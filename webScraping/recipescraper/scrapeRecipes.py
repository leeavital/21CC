#!/usr/bin/env python
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log, signals, project
from recipescraper.spiders.recipe_spider import RecipeSpider
from scrapy.xlib.pydispatch import dispatcher

def stop_reactor():
  reactor.stop()

def getRecipe(url):
  dispatcher.connect(stop_reactor,signal=signals.spider_closed)
  spider=RecipeSpider(startURL=url)
  crawler=Crawler(Settings())
  crawler.configure()
  crawler.crawl(spider) 
  crawler.start()
  log.start()
  #log.message('Running.')
  reactor.run()
 # log.message('Stopped')

#getRecipe("http://allrecipes.com/Recipe/Apple-Pie-2/")
