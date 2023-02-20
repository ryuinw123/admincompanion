from django.db import models

# Manager
class AndroidDatabaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('android')