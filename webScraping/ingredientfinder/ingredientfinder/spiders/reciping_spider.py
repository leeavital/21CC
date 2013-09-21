from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from ingredientfinder.items import IngredientItem
class IngredientSpider(CrawlSpider):
  name="reciping"
  allowed_domains=["allrecipes.com"]
  start_urls=["http://allrecipes.com/recipe/Slow-Cooker-Apple-Crisp/"]
  
#  rules=(
 # Rule(SgmlLinkExtractor(allow=('recipe\.aspx',)),callback='parse_ingredient'),
#  )

  def parse_ingredient(self,response):
    hxs=HtmlXPathSelector(response)
    sites=hxs.select('//ul[@class="ingredient-wrap"]/li')
    items=[]
    for site in sites:
      item=IngredientItem()
      item['ingName']=site.select('//span[@class="ingredient-name"]').extract()
      print ingName
      items.append(item)
      return items
