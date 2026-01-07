from django.apps import AppConfig


"""
Configuration for the 'document' Django app.

- Defines the app name as 'document'.
- Sets the default type of primary key for models in this app 
  to BigAutoField (large integer auto-incrementing ID).
- This class is used by Django to configure app-specific settings 
  and metadata.
"""


class DocumentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "document"
