from django.apps import AppConfig

class ICSwebtrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'icswebtracker'
    verbose_name = 'Web Traffic Tracker'

    def ready(self):
        """
        Perform initialization tasks when the app is ready.
        """
        # Import signals or perform other setup if needed
        pass