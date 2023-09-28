from django.apps import AppConfig


class TableConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'table'

    def ready(self) -> None:
        print('come to ready')
        import table.signals
