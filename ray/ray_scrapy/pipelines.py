# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re

# from scrapy.exporters import CsvItemExporter

from ray_scrapy.lib import get_db_session_and_base


class ReviewAnalysisPipeLine(object):

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        return pipeline

    def open_spider(self, spider):
        # self.file = open(review_output_file, 'w+b')
        # self.exporter = CsvItemExporter(self.file)
        # self.exporter.start_exporting()

        self.db_session, self.db_base = get_db_session_and_base()
        self.db_reviews_model = self.db_base.classes.reviews_review
        self.db_topics_models = self.db_base.classes.topics_topic
        self.db_reviews_review_topic = self.db_base.classes.reviews_review_topic
        self.topics_dict = {}
        for x in self.db_session.query(self.db_topics_models).all():
            self.topics_dict[x.keyword.lower()] = x.id
            
        re_search_keywords = [r"\b" + x + r"\b" for x in self.topics_dict.keys()]
        self.re_search_obj = re.compile(r'{0}'.format(
            "|".join(re_search_keywords)), re.I)

    def close_spider(self, spider):
        # self.exporter.finish_exporting()
        # self.file.close()
        # self._ssession.commit()
        self.db_session.close()

    def process_item(self, item, spider):
        self.update_sentiment(item)
        # self.exporter.export_item(item)
        review = self.db_reviews_model(
            product_id=spider.product_no, 
            rating=float(item['rating']), 
            review_text=item['review_text'],
            title=item['title'],
            review_date=item['review_date']
        )
        self.db_session.add(review)
        self.db_session.commit()
        
        # map topics
        self.update_topics(review.review_text, review.id)

        return item

    def update_topics(self, text, review_id):
        if not text:
            return []
        result = self.re_search_obj.findall(text)
        # convert caps of the found keyword to title so they look uniform 
        # rather than user mentioned case and eliminate duplicates
        # if the review has same keyword mentioned multiple times
        # sort the keywords, so they look unique
        
        if result:
            final_result = []
            for x in result:
                y = x.strip().lower()
                if y not in final_result:
                    final_result.append(y)
                    topic_id = self.topics_dict[y]
                    t = self.db_reviews_review_topic(review_id=review_id, topic_id=topic_id)
                    self.db_session.add(t)
            self.db_session.commit()

    def update_sentiment(self, item):
        sentiment = "Positive" if item['rating'] > float(3.0) else "Negative"
        item['rating_sentiment'] = sentiment