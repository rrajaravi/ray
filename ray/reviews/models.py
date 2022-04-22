from django.db import models

from topics.models import Topic as topic_model
from products.models import Product as product_model
# Create your models here.

class Review(models.Model):
    product = models.ForeignKey(product_model, related_name='product', on_delete=models.CASCADE, null=True, blank=True)
    topic = models.ManyToManyField(topic_model, related_name='topic')
    rating = models.FloatField()
    review_date = models.CharField(max_length=100)
    review_text = models.TextField()
    title = models.CharField(max_length=200)

