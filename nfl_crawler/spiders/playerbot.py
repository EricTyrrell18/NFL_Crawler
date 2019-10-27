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
        player_item = PlayerItem()
        player_item["name"] = response.css("span.player-name::text").extract_first().strip()
        player_item["identifier"] = response.url.split("/")[5]
        player_item["headers"] = response.css("table").css("thead tr.player-table-key td::text").extract()
        player_item["data"] = dict()
        # Recursively update the PlayerItem with multiple years of data
        url_to_format = response.url+"?season={}"
        yield scrapy.Request(url_to_format.format(years[0]), callback=self.process_tables, cb_kwargs=dict(year = years[0], player = player_item, years_remaining = years[1:], url_base = url_to_format )) 

    def process_tables(self, response, year, player, years_remaining, url_base):
        
        # Select all tables. Could be several such as preseason, regular season, post season, probowl 
        raw_tables = response.css("table")
        table_data = dict()      
        # Grab preseason, regular season, post season, probowls, and whatever else there is
        for table in raw_tables:
            # Pull the name of the table to use as an identified
            table_name = table.css("thead tr:first-child td:first-child::text").extract_first()
            
            rows = table.css("tbody tr")
            # Remove rows which don't contain any information 
            rows = [x for x in rows if x.css("td::text").extract_first()]
            # Remove the "total" row because it complicates things
            rows = rows[:-1]

            weekly_data = dict()
            for row in rows:
                cur_week = row.css("td:nth-child(1)::text").extract_first()
                cur_date = row.css("td:nth-child(2)::text").extract_first()
                # Regex is required because extracting is interacting wierdly with the whitespace here
                # TODO: extend regex to include the "@" which signifies an away game
                # possibly generate an additional header for this 
                cur_opp = row.css("td:nth-child(3) a::text").re_first("[A-Za-z]{2,3}")
                final_score = row.css("td:nth-child(4)").re_first("\d+\-\d+")

                # Collect the rest of the data
                stats = row.css("td:nth-child(n+5)::text").extract()
                # TODO: Determine if this is a good approach. Perhaps it should ignore games the player didn't play which would substantially reduce the 0's in a players dataset.
                stats = [stat if stat != "--" else "0.0" for stat in stats]

                weekly_data[cur_week] = [cur_date, cur_opp, final_score] + stats

            table_data[table_name] = weekly_data

        player["data"][year] = table_data
        if years_remaining:
            yield scrapy.Request(url_base.format(years_remaining[0]), callback=self.process_tables, cb_kwargs=dict(year = years_remaining[0], player = player, years_remaining = years_remaining[1:], url_base = url_base))
        else:
            yield player
