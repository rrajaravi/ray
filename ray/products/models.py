import re

from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ray_scrapy.lib import get_product_name_by_url, get_reviews_by_product

# Create your models here.

class ProductType(models.Model):
    name = models.CharField(max_length=100)
    sample_url = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = models.ForeignKey('ProductType', related_name='product_type', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    product_id = models.CharField(max_length=1000, blank=True)
    url = models.CharField(max_length=200, unique=True)

    def clean(self):
        if "amazon.com" in self.url:
            # Update Name
            result = re.search(r'/(\w+)$', self.url)
            if result:
                self.product_id = result.group(1)
            else:
                raise ValidationError(_('Unable to extract product id from the given url: {}'.format(self.url)))

            product_name = get_product_name_by_url(self.url)
            self.name = product_name
        elif "bestbuy.com" in self.url:
            result = re.search(r'/(?P<product_name>[-\w]+)/(?P<product_id>\d+)', self.url)

            if result:
                self.product_id = result.group('product_id')
                self.name = result.group('product_name')
            else:
                raise ValidationError(_('Unable to extract product id from the given url: {}'.format(self.url)))
        
        else:
            raise ValidationError(_('Unable to extract product id and name from the given url: {}'.format(self.url)))

    def __str__(self):
        return self.name

@receiver(signals.post_save, sender=Product)
def create_product(sender, instance, created, **kwargs):
    get_reviews_by_product(instance)
