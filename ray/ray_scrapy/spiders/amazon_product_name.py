import math
import re

# import scrapy
# from ray_scrapy.items import AmazonProductName


# class AmazonProductNameSpider(scrapy.Spider):
#     name = 'amazon_product_name'
#     start_urls = []

#     def parse(self, response):
#         amazon_product_name = AmazonProductName()
#         product_name = response.css(
#             'span[id="productTitle"]::text').extract_first()
#         amazon_product_name['name'] = product_name.strip()
#         yield amazon_product_name
