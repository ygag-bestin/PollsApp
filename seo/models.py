from django.db import models
from taggit.managers import TaggableManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.apps import apps
from model_utils.managers import InheritanceManager
from django.contrib.auth import get_user_model

from django.db.models.signals import post_save
from django.dispatch import receiver



class SeoMetaData(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=155)
    url = models.CharField(max_length=255)
    user = get_user_model()

    class Meta:
        abstract = True

    # content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')

    # def save(self, *args, **kwargs):
    #     if self._state.adding:
    #         self.real_type = self._get_real_type()
    #     super(SeoMetaData, self).save(*args, **kwargs)
    #
    # def _get_real_type(self):
    #     return ContentType.objects.get_for_model(type(self))
    #
    # def cast(self):
    #     return self.real_type.get_object_for_this_type(pk=self.pk)


class SeoList(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def display(self):
        ListObjects = SeoList.objects.filter(id=self.object_id).values('seo2__title')
        return ListObjects
