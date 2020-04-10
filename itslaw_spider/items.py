# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItslawDetailSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    fullJudgement = scrapy.Field()
    # temporaryJudgementsCount = scrapy.Field()
    # cacheType = scrapy.Field()
