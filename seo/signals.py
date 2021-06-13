from .models import SeoList
from polls.models import Question
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Question)
def SeoList_handler(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs.get('created', True):
        ctype = ContentType.objects.get_for_model(instance)
        SeoList.objects.create(
            content_type=ctype,
            object_id=instance.id,
        )
