from django.db import models

class StoreStatus(models.Model):
    store_id = models.CharField(max_length=200)
    timestamp_utc = models.CharField(max_length=200)
    status = models.CharField(max_length=200)