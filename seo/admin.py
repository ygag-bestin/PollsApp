from django.contrib import admin
from .models import SeoMetaData


class SeoMetaDataAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'url', 'tag_list']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())



admin.site.register(SeoMetaData, SeoMetaDataAdmin)

