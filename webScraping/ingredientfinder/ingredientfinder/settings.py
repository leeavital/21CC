# Scrapy settings for ingredientfinder project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'ingredientfinder'

SPIDER_MODULES = ['ingredientfinder.spiders']
NEWSPIDER_MODULE = 'ingredientfinder.spiders'
ITEM_PIPELINES='ingredientfinder.pipelines.IngredientfinderPipeline'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ingredientfinder (+http://www.yourdomain.com)'
