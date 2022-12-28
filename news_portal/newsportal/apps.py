from django.apps import AppConfig


class NewsportalConfig(AppConfig):
    name = 'newsportal'

    def ready(self):
        import newsportal.signals
