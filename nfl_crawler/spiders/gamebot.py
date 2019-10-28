# -*- coding: utf-8 -*-
import scrapy
import logging
from itertools import product
from nfl_crawler.items import NflGameItem

class GamebotSpider(scrapy.Spider):
    name = 'gamebot'
    allowed_domains = ['nfl.com']

    def start_requests(self):
        base_url = 'http://www.nfl.com/schedules/{}/REG{}'
        years = list(range(1995,2019))
        games = list(range(18))[1:]
        # go through all the combinations
        for comb in product(years,games):
            yield scrapy.Request(base_url.format(comb[0], comb[1]), callback=self.parse) 

    def parse(self, response):

        # This isn't gonna be pretty, but it seemingly worked
        # Grab the days games are played on.
        days = response.xpath('//li[@class="schedules-list-date"]/span/span/text()').extract()
        logging.debug(days)
        # recursively grab data between the bounds of the first date and the last date
        while len(days) >= 2:
            # Most of the game data's between two dates.
            # The date's are also at the same level as the games, so it's hard to use pure css to grab the info correctly
            # think of it as before this date and after this other date 
            xpath_query = '//li[following-sibling::li[.//span/text()="{}"]][preceding-sibling::li[.//span/text()="{}"]]'.format(days[1], days[0])

            teams = response.xpath(xpath_query)

            # TODO: make a function to remove redundancy
            away_teams = teams.css("span.team-name.away::text").extract()
            home_teams = teams.css("span.team-name.home::text").extract()
            away_scores = teams.css("span.team-score.away::text").extract()
            home_scores = teams.css("span.team-score.home::text").extract()
            stadium = teams.xpath('./div/@data-site').extract()

            game_stats  = list(zip(away_teams, home_teams, away_scores, home_scores, stadium))

            for game in game_stats:
                  item =  NflGameItem()
                  item["away_team"] = game[0]
                  item["home_team"] = game[1]
                  item["away_score"] = game[2]
                  item["home_score"] = game[3]
                  item["stadium"] = game[4]
                  item["date"] = days[0]
                  item["year"] = response.url.split("/")[4]
                  yield item
            # move on to the next day
            days = days[1:]

        # still a single day left, but it's an easy cleanup
        # TODO: make a function to remove redundancy
        teams = response.xpath('//li[preceding-sibling::li[.//span/text()="{}"]]'.format(days[0]))
        away_teams = teams.css("span.team-name.away::text").extract()
        home_teams = teams.css("span.team-name.home::text").extract()
        away_scores = teams.css("span.team-score.away::text").extract()
        home_scores = teams.css("span.team-score.home::text").extract()
        stadium = teams.xpath('./div/@data-site').extract()
        
        game_stats  = list(zip(away_teams, home_teams, away_scores, home_scores, stadium))
        logging.debug(game_stats)
        for game in game_stats:
            item =  NflGameItem()
            item["away_team"] = game[0]
            item["home_team"] = game[1]
            item["away_score"] = game[2]
            item["home_score"] = game[3]
            item["stadium"] = game[4]
            item["date"] = days[0]
            item["year"] = response.url.split("/")[4]
            yield item
        
