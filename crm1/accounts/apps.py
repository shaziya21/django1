from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):          # overriding ready method
        import accounts.signals   # import(app name.signals)
