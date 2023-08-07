from django.urls import path
from .views import TriggerReport, GetReport

urlpatterns = [
    path('trigger_report', TriggerReport.as_view()),
    path('get_report', GetReport.as_view()),
]
