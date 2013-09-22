from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from recipescraper.items import RecipescraperItem

class RecipeSpider(BaseSpider):
  name="recrawling"
 
  def __init__(self,category=None,domain=None,startURL="http://allrecipes.com/Recipe/Apple-Pie-2/"):
    self.domain=["allrecipes.com"]
    self.start_urls=[startURL]

  def parse(self,response):
    hxs=HtmlXPathSelector(response)
    sites=hxs.select('//ol/li')
    items=[]
    count=0
    for site in sites:
      item=RecipescraperItem()
      item['recipe']=sites.select('//span[@class="plaincharacterwrap break"]/text()').extract()[count]
      items.append(item)
      count=count+1
    return items
    
   
