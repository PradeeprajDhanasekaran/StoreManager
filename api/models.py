
from django.db import models

class StoreStatus(models.Model):
    store_id = models.CharField(max_length=50)
    timestamp_utc = models.DateTimeField()
    status = models.CharField(max_length=10)

class StoreHours(models.Model):
    store_id = models.CharField(max_length=50)
    day = models.IntegerField()
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

class StoreTimezone(models.Model):
    store_id = models.CharField(max_length=50)
    timezone_str = models.CharField(max_length=50)
class ReportStatus(models.Model):
    report_id = models.CharField(max_length=50)
    status = models.IntegerField(help_text='0 means running and 1 means completed')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)