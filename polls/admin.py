from django.contrib import admin
from django import forms
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .forms import VerifyTagAdmin
from .models import User
from django.contrib.auth.admin import UserAdmin
from .models import Question, Choice, Comment, Tag
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.db.models.functions import Lower


class ChoiceFormSet(BaseInlineFormSet):

    def clean(self):
        super(ChoiceFormSet, self).clean()
        if any(self.errors):
            return

        choice_texts = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                choice_text = form.cleaned_data['choice_text'].lower()

                if choice_text:
                    if choice_text in choice_texts:
                        duplicates = True
                    choice_texts.append(choice_text)
                if duplicates:
                    raise forms.ValidationError(
                        'Choice Already Exists !.'
                    )


class ChoiceInline(admin.TabularInline):
    model = Choice
    min_num = 2
    formset = ChoiceFormSet


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 1


class TagQuestionInline(admin.TabularInline):
    model = Question.tag.through
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ('added_by', {'fields': ['added_by']}),
        ('priority', {'fields': ['priority']}),
        ('expiry date', {'fields': ['expiry_date']}),
        ('tag', {'fields': ['tag']}),
    ]
    inlines = [ChoiceInline, CommentInLine, ]
    list_display = ('id','question_text', 'pub_date', 'was_published_recently', 'choices', 'added_by',)
    search_fields = ['question_text']

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


class TagAdmin(admin.ModelAdmin):
    form = VerifyTagAdmin
    list_display = ('tag',)
    inLines = [TagQuestionInline]


admin.site.register(Question, QuestionAdmin, )
admin.site.register(Tag, TagAdmin)
