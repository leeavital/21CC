# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.contrib.exporter import XmlItemExporter

class IngredientfinderPipeline(object):

  def __init__(self):
    self.files={}

  @classmethod 
  def from_crawler(cls,crawler):
    pipeline=cls()
    crawler.signals.connect(pipeline.spider_opened,signals.spider_opened)
    crawler.signals.connect(pipeline.spider_closed,signals.spider_closed)
    return pipeline

  def spider_opened(self,spider):
    file=open('recipes.xml','w+b')
    self.files['recipes']=file
    file.write('\n'+spider.name+'\n')
    self.exporter=XmlItemExporter(file)
    self.exporter.start_exporting() 
    file.write('\n')

  def spider_closed(self,spider):
    self.exporter.finish_exporting()
    #file= self.files.pop(spider)
    file=self.files['recipes']
    file.close()
    
  def process_item(self, item, spider):
    self.exporter.export_item(item)
    return item
