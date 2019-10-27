# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import re
import logging
class NflCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class DuplicatePipeline(object):
    player_url_set = set()
    def process_item(self, item, spider):
        if item["player_url"] in self.player_url_set:
            raise DropItem("Duplicate playerURL found: {}".format(item["player_url"]))
        else:
            self.player_url_set.update(item["player_url"])
            return item


class PlayerItemPipeline(object):
    """Replace missing data with 0's"""
    def process_item(self, item, spider):
        
        return item
