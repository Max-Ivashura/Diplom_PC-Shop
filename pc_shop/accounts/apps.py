# accounts/apps.py
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        # Импортируем сигналы здесь, чтобы избежать циклических зависимостей
        import accounts.signals  # noqa