# Scrapy settings for recipescraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'recipescraper'

SPIDER_MODULES = ['recipescraper.spiders']
NEWSPIDER_MODULE = 'recipescraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'recipescraper (+http://www.yourdomain.com)'
