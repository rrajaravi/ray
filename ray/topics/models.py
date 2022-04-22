from django.db import models

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    keyword = models.CharField(max_length=100)
    case_sensitivity = models.BooleanField(default=False)

    def __str__(self):
        return self.name
