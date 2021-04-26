from django.db import models
import datetime
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Tag(models.Model):
    """
        Stores a tag for each question, related (ManyToMany relation)to :model:`Question`
    """
    tag = models.CharField(max_length=20)

    def __str__(self):
        return self.tag


class Question(models.Model):
    """
        Stores a single poll question entry, related to :model:`Choice` and
        :model:`Tag`.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    view_count = models.IntegerField(default=1, null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, default=None)
    tag = models.ManyToManyField(Tag, related_name="tags", blank=True)
    priority = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        """Makes the poll question entry live on the site."""
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def choices(self):
        count_choice = self.choice.all().count()
        return count_choice

    @property
    def is_expired(self):
        now = timezone.now()
        if self.expiry_date > now:
            return False
        else:
            return True


class Choice(models.Model):
    """
        Stores choice entries for each question, related to :model:`Question`
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='choice')
    choice_text = models.CharField(max_length=200, null=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    # def __str__(self):
    #     template = '{0.choice_text} : {0.votes}'
    #     return template.format(self)


class Comment(models.Model):
    """
        Stores a comment for each question, related to :model:`Question`
    """
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='comments')
    email = models.EmailField()
    body = models.TextField()

    def __str__(self):
        return 'Comment by {} on {}'.format(self.email, self.question)
