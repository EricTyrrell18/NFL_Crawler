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
	data = scrapy.Field()

class NflGameItem(scrapy.Item):
	year = scrapy.Field()
	date = scrapy.Field()
	away_team = scrapy.Field()
	home_team = scrapy.Field()
	away_score = scrapy.Field()
	home_score = scrapy.Field()
	stadium = scrapy.Field()
