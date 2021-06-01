from django.db import models
from taggit.managers import TaggableManager


class SeoMetaData(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=155)
    tags = TaggableManager()
    url = models.CharField(max_length=255)
