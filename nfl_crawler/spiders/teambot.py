# -*- coding: utf-8 -*-
import scrapy
import itertools
from nfl_crawler.items import NflPlayerURLItem
class TeambotSpider(scrapy.Spider):
    name = 'teambot'
    allowed_domains = ['nfl.com']
    team_profiles = ["NE", "NYG", "MIN", "PHI", "NYJ", "DAL", "GB", "OAK", "KC", "ATL",
            "LA", "HOU", "JAX", "CLE", "TB", "NO", "DEN",  "WAS", "CAR", "TEN",
            "CIN", "LAC", "DET", "SEA", "IND", "BUF", "SF","PIT", "CHI" ,"MIA",
             "BAL", "ARI" ]
    years = list(range(2005,2020))
    url_params = itertools.product(years, team_profiles)
    url_str = "http://www.nfl.com/teams/statistics?season={}&team={}"
    
    def start_requests(self):
        start_urls = [self.url_str.format(param[0], param[1]) for param in self.url_params]
        for url in start_urls:
            yield scrapy.Request(url, callback = self.parse)

    def parse(self, response):
        #Selector for collecting Links to players
        # convert to a set to remove duplicates
        players = response.css("td.first a::attr(href)").extract()

        for link in players:
            yield NflPlayerURLItem(player_url = link)


