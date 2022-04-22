# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ReviewanalysisItem(scrapy.Item):
    rating_sentiment = scrapy.Field()
    matched_keywords = scrapy.Field()
    product = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    review_text = scrapy.Field()
    review_date = scrapy.Field()