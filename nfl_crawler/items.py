# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NflCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NflPlayerURLItem(scrapy.Item):
	player_url = scrapy.Field()

class PlayerItem(scrapy.Item):
	identifier = scrapy.Field()
	name = scrapy.Field()
	year = scrapy.Field()
	headers = scrapy.Field()
	rows = scrapy.Field()
