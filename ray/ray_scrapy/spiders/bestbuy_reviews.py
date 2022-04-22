import json

import scrapy
from ray_scrapy.items import ReviewanalysisItem

class BestbuyReviewSpider(scrapy.Spider):
    name = 'bestbuy'

    def __init__(self, url=None, bestbuy_base_url=None, product_no=None, *args, **kwargs):
        super(BestbuyReviewSpider, self).__init__(*args, **kwargs)
        # custom attributes 
        self.product_no = product_no
        self.bestbuy_base_url = bestbuy_base_url
        self.start_urls = isinstance(url, list) and url or [url]

    def parse(self, response):
        review = ReviewanalysisItem()
        next_page = response.css('li[class="page next"]')
        next_page = next_page.css('a::attr(href)').extract_first()

        reviews = self.get_reviews(response)
        for x in reviews:
            review['rating'] = x['rating']
            review['review_date'] = x['review_date']
            review['review_text'] = x['review_body']
            review['title'] = x['subject']
            yield review

        if next_page:
            next_url = self.bestbuy_base_url + str(next_page)
            yield scrapy.Request(next_url, callback=self.parse)

    def get_reviews(self, response):
        reviews = list()
        reviews_list_tag = response.css('ul.reviews-list')
        reviews_list = reviews_list_tag.css('li.review-item')
        for review in reviews_list:
            review_data = dict()

            review_script = review.css('script[type="application/ld+json"]::text').extract_first()
            review_item = json.loads(review_script)
            
            body = review_item['reviewBody']
            subject = review_item['name']
            rating = review_item['reviewRating']['ratingValue']

            review_data["rating"] = float(rating)
            review_data["subject"] = self.escape(subject)
            review_date = review.css(
                'time.submission-date::attr(title)').extract_first()
            review_data["review_date"] = review_date
  
            review_body = self.concate_review_bestbuy(body)
            review_data["review_body"] = review_body
            reviews.append(review_data)

        return reviews

    @staticmethod
    def escape(text):
        text = text.strip()
        return text

    @staticmethod
    def concate_review_bestbuy(review):
        data = review.replace("\n", " ")
        data = data.replace("\r", "")
        return data
