from django.contrib.sitemaps import Sitemap
from polls.models import Question


class QuestionSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    protocol = 'http'

    def items(self):
        return Question.objects.all()

    def location(self, item):
        return item
