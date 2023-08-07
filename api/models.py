
from django.db import models

class StoreStatus(models.Model):
    store_id = models.IntegerField()
    timestamp_utc = models.DateTimeField()
    status = models.CharField(max_length=10)

class StoreHours(models.Model):
    store_id = models.IntegerField()
    day_of_week = models.IntegerField()
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

class StoreTimezone(models.Model):
    store_id = models.IntegerField()
    timezone_str = models.CharField(max_length=50)
