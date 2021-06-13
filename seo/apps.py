from django.apps import AppConfig


class SeoConfig(AppConfig):
    name = 'seo'

    def ready(self):
        import seo.signals
