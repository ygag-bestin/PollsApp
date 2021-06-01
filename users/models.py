from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db.models.functions import Lower
from graphene_django import DjangoObjectType
from django.conf import settings
from django.conf.urls.static import static


class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """

    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        if isinstance(value, str):
            return value.lower()
        return value


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
        to change username field to email field
    """
    username = None
    email = LowercaseEmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    dob = models.DateField(null=True, default=None, blank=True)
    nickname = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to="pro_pic/", null=True, blank=True)

    def image_tag(self):
        if self.image:
            img_url = self.image.url

        else:
            img_url = settings.STATIC_URL + 'polls/images''/default.jpeg'

        return format_html('<img src="{}" width="100px" height="100px" />'.
                           format(img_url))

    image_tag.allow_tags = True

    image_tag.short_description = 'Image'
    objects = UserManager()

