# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DartsItem(scrapy.Item):
    # define the fields for your item here like:
    tournamentName = scrapy.Field()
    gameDate = scrapy.Field()
    playersNames = scrapy.Field()
    score = scrapy.Field()
    player1Odds = scrapy.Field()
    player2Odds = scrapy.Field()

    player1 = scrapy.Field()
    player1Initial = scrapy.Field()
    player2 = scrapy.Field()
    player2Initial = scrapy.Field()
    outcome = scrapy.Field()
    pass
