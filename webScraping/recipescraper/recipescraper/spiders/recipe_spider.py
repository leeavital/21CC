from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
class RecipeSpider(BaseSpider):
  name="recrawling"
 
  def __init__(self,category=None,domain=None,startURL="http://allrecipes.com/Recipe/Apple-Pie-2/"):
    self.domain=["allrecipes.com"]
    self.start_urls=[startURL]

  def parse(self,response):
    hxs=HtmlXPathSelector(response)
    sites=hxs.select('//ol/li')

    recipe=sites.select('//span[@class="plaincharacterwrap break"]/text()').extract()
    return recipe[0]
    
   
