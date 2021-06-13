from django.contrib import admin
from .models import SeoList
from polls.models import Question


#
class SeoListAdmin(admin.ModelAdmin):
    list_display = ('display',)




    # def get_queryset(self, request):
    #     return super().get_queryset(request).prefetch_related('tags')
    #
    # def tag_list(self, obj):
    #     return u", ".join(o.name for o in obj.tags.all())


admin.site.register(SeoList, SeoListAdmin)
# admin.site.register(SeoMetaData,SeoMetaDataAdmin)
