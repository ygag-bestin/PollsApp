from .models import Comment, Choice, Tag
from django import forms
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm

User = get_user_model()


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea,
                           error_messages={
                               'required': 'Please Comment Something'
                           })

    class Meta:
        model = Comment
        fields = ['email', 'body']


class VerifyTagAdmin(forms.ModelForm):

    class Meta:
        model = Tag
        fields = '__all__'

    def clean_tag(self):
        tag = self.cleaned_data['tag'].lower()
        for instance in Tag.objects.all().exclude(id=self.instance.id):
            if instance.tag == tag:
                raise forms.ValidationError('tag already exists')
        return tag
