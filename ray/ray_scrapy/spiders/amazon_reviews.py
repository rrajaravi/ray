import math
import re

import scrapy
from ray_scrapy.items import ReviewanalysisItem

class AmazonReviewSpider(scrapy.Spider):
    name = 'amazon'

    def __init__(self, url=None, amazon_base_url=None, product_no=None, *args, **kwargs):
        super(AmazonReviewSpider, self).__init__(*args, **kwargs)
        # custom attributes 
        self.product_no = product_no
        self.amazon_base_url = amazon_base_url
        self.start_urls = isinstance(url, list) and url or [url]

    def parse(self, response):
        review = ReviewanalysisItem()
        next_page = response.css('li.a-last')
        next_page = next_page.css('a::attr(href)').extract_first()

        reviews = self.get_reviews(response)
        for x in reviews:
            review['rating'] = x['rating']
            review['review_date'] = x['review_date']
            review['review_text'] = x['review_body']
            review['title'] = x['subject']
            yield review

        if next_page:
            next_url = self.amazon_base_url + str(next_page)
            yield scrapy.Request(next_url, callback=self.parse)

    def get_reviews(self, response):
        reviews = list()
        reviews_list_tag = response.css('div[id="cm_cr-review_list"]')
        reviews_list = reviews_list_tag.css('div[data-hook="review"]')
        for review in reviews_list:
            review_data = dict()
            rating = review.css(
                'span[class="a-icon-alt"]::text').extract_first()
            review_data["rating"] = float(
                rating.replace(" out of 5 stars", ""))
            subject = review.css('a[data-hook="review-title"]')
            subject = subject.css('span::text').extract_first()
            review_data["subject"] = self.escape(subject)
            review_date = review.css(
                'span[data-hook="review-date"]::text').extract_first()
            review_data["review_date"] = review_date.replace("on ", "")
            review_body = review.css('span[data-hook="review-body"]')
            review_body = review_body.css('span::text').extract()
            review_body = self.concate_review(review_body)
            review_data["review_body"] = self.escape(review_body)
            reviews.append(review_data)

        return reviews

    @staticmethod
    def escape(text):
        text = text.strip()
        return text

    @staticmethod
    def concate_review(review):
        data = "<br>".join(x for x in review)
        return data.replace('<br>', '')
