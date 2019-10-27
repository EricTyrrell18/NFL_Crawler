# -*- coding: utf-8 -*-
import scrapy
import logging
from nfl_crawler.items import PlayerItem

class PlayerbotSpider(scrapy.Spider):
    name = 'playerbot'
    allowed_domains = ['nfl.com']
    start_urls = ['http://nfl.com/']
    base_url = "http://nfl.com"

    def start_requests(self):
        #Create initial requests
        with open('/Users/cicero222/Desktop/programming/python/nfl/nfl_crawler/test_player_urls.txt','r') as f:
            for path in f.readlines():
               yield scrapy.Request(self.base_url+path, callback=self.parse) 

    def parse(self, response):
        # We should recieve an easier url to work with
        # We'll modify this new url to navigate to game logs
        new_url = response.url[:-7]+ "gamelogs"
        yield scrapy.Request(new_url, callback=self.parse_player)
    

    def parse_player(self, response):
        #Selector for looking at all seasons player
        years = response.css("option::attr(value)").extract()
        logging.warning(years)                
        # format of data should look like [[2000, [1,23,21,231]],[2001,[12324,214,11]]]
        for y in years:
            yield scrapy.Request(response.url+"?season={}".format(y), callback=self.process_tables, cb_kwargs=dict(year=y)) 

    def process_tables(self, response, year):
        year_item = PlayerItem()
        year_item["year"] = year
        year_item["name"] = response.css("span.player-name::text").extract_first().strip()
        year_item["identifier"] = response.url.split("/")[5]
        # select all tables. Could be several such as preseason, regular season, post season, probowl 
        raw_tables = response.css("table")
        table = raw_tables        
        # We only care about the regular season
        for t in raw_tables:
            if t.css("thead tr td::text").extract_first() == "Regular Season":
                table = t
            else:
                logging.log(logging.ERROR, "No Regular Season Found{}".format(response.url) )
        #Selector for extracting column headers
        #Players will have different column headers dependent on position
        #Week will be the key in the dictionary, so it can be ignored
        year_item["headers"] = response.css("table").css("thead tr.player-table-key td::text").extract()
        # Selector for extracting each row
        rows = table.css("tbody tr")
    
        # get rid of empty rows which are used for formatting
        rows = [x for x in rows if x.css("td::text").extract_first()] 
        # get rid of last row because it is unneeded
        # the last row is unneeded because it's the total of the previous rows
        # and it would complicate things further to scrape
        rows = rows[:len(rows)-1]
        weekly_data = []        
        for row in rows:
            # collect the first two columns: week and Game Date
            cur_week = row.css("td:nth-child(1)::text").extract_first()
            cur_date = row.css("td:nth-child(2)::text").extract_first()
            
            # the next two columns have an odd format and need separate selectors
            # handle Opp
            # this doesn't select the exact opponent, but can be cleaned up in the item pipeline (ie strip())
            cur_opp = row.css("td:nth-child(3) a::text").re_first("[A-Za-z]{2,3}")

            # handle Result
            # same as before. Format in pipeline
            final_score = row.css("td:nth-child(4)").re_first("\d+\-\d+")

            # collect the rest of the columns
            stats = row.css("td:nth-child(n+5)::text").extract()
            # "--" means they didn't have a statline for this stat this week
            # TODO: determine if this is a mistake which will have an impact on analysis.
            # because of the difference between a natural 0 and a dnp or injury
            stats = [stat if stat != "--" else "0.0" for stat in stats]
            #combine all the columns together
            columns = [cur_week, cur_date, cur_opp, final_score] + stats 
            weekly_data.append(columns)
        year_item["rows"] = weekly_data
        yield year_item
