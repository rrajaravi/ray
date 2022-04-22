import os
import requests

from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from scrapyd_api import ScrapydAPI
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


DB_CONFIG_FILE = os.path.expanduser('~/ray_mysql.config')
scrapyd = ScrapydAPI('http://localhost:6800')
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def get_product_name_by_url(url):
    product_name = ' '
    r  = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find("meta", {"name": "keywords"})
    if s:
        product_name = s.get("content").split(',')[0]
    return product_name

def get_reviews_by_product(product):
    if 'amazon.com' in product.url:
        return get_amazon_reviews(product)
    elif 'bestbuy.com' in product.url:
        return get_bestbuy_reviews(product)
    else:
        raise ValidationError(_('Unknown product type: {}'.format(product.product_type)))

def get_amazon_reviews(product):
    amazon_base_url = "https://www.amazon.com/"
    amazon_product_review_uri = "product-reviews/"
    product_url = amazon_base_url + amazon_product_review_uri + product.product_id
    print("Trying to get reviews from URL: {}".format(product_url))
    
    response = scrapyd.schedule(
        'ray_scrapy',
        'amazon', 
        url=product_url, 
        product_no=product.id,
        amazon_base_url=amazon_base_url,
    )
    print(response)

def get_bestbuy_reviews(product):
    bestbuy_base_url = "https://www.bestbuy.com/"
    bestbuy_product_review_uri = "site/reviews/"
    product_url = bestbuy_base_url + bestbuy_product_review_uri + product.name + "/" + product.product_id
    print("Trying to get reviews from URL: {}".format(product_url))
    
    response = scrapyd.schedule(
        'ray_scrapy',
        'bestbuy', 
        url=product_url, 
        product_no=product.id,
        bestbuy_base_url=bestbuy_base_url,
    )
    print(response)

def get_db_url_by_config(configfile):
    db_config = {}
    with open(configfile, 'r') as f:
        for line in f:
            if '=' in line:
                k, v = line.split('=')
                db_config[k.strip()] = v.strip()
    
    db_url = "mysql://{}:{}@{}:3306/{}".format(
        db_config['user'],
        db_config['password'],
        db_config['host'],
        db_config['database']
    )
    return db_url

def get_db_engine():
    engine_url = get_db_url_by_config(DB_CONFIG_FILE)
    engine = create_engine(engine_url)
    return engine

def get_db_session_and_base():
    # create db engine
    engine = get_db_engine()

    # create our own metadata
    metadata = MetaData()

    # limit only what tables needed to reflect in metadata
    metadata.reflect(engine)#, only=['accounts_user'])

    # we can then produce a set of mappings from this MetaData.
    Base = automap_base(metadata=metadata)

    # calling prepare() just sets up mapped classes and relationships.
    Base.prepare()

    session = sessionmaker(bind=engine)()
    return (session, Base)
