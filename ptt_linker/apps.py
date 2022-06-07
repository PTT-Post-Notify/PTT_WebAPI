from django.apps import AppConfig


class PttLinkerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ptt_linker'
    from django.core.cache import cache
    cache.set('CacheInit', True, None)
