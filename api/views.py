from background_task import background
from django.http import FileResponse, HttpResponse
import pandas as pd
from django.utils import timezone
from datetime import timedelta
from .models import StoreStatus, StoreHours, StoreTimezone, ReportStatus
from .serializers import StoreStatusSerializer, StoreHoursSerializer
from rest_framework.views import APIView,Response
from rest_framework.decorators import api_view
from rest_framework import status
import time
from .management.commands.import_csv import Command
import datetime
import uuid
from StoreManager.settings import BASE_DIR
@background(schedule=0)
def generate_report(report_id):
    # Retrieve data from the database for each store
    print('task started')
    new_status = ReportStatus.objects.create(report_id=report_id, status=0, start_time=timezone.now())
    time.sleep(15)
    print('task ended')
   # --------------------------------------------------------------------------
import pandas as pd
from datetime import datetime, timedelta
import pytz
from django.db import connection
from myapp.models import StoreStatus, StoreHours, StoreTimezone

# Define your Django models
# ...

# Function to generate the report
def generate_report():
    # Get the current time in UTC (using the max timestamp among all observations)
    max_timestamp = StoreStatus.objects.latest('timestamp_utc').timestamp_utc
    current_time_utc = max_timestamp

    # Retrieve data from the database
    store_activity_data = StoreStatus.objects.all()
    business_hours_data = StoreHours.objects.all()
    timezone_data = StoreTimezone.objects.all()

    # Calculate time intervals for the last hour, last day, and last week
    last_hour = current_time_utc - timedelta(hours=1)
    last_day = current_time_utc - timedelta(days=1)
    last_week = current_time_utc - timedelta(weeks=1)

    # Calculate business hours extrapolation based on observations
    def extrapolate_time_series(observations, start_time, end_time):
        if not observations:
            return []

        intervals = []
        current_time = start_time
        for obs in observations:
            interval = (current_time, obs['timestamp_utc'], obs['status'])
            intervals.append(interval)
            current_time = obs['timestamp_utc']
        
        if current_time < end_time:
            intervals.append((current_time, end_time, observations[-1]['status']))

        time_series = []
        for start, end, status in intervals:
            time_series.extend(pd.date_range(start, end, freq='T').tolist())
        
        return time_series

    # Calculate extrapolated uptime and downtime using business hours
    def calculate_extrapolated_uptime_downtime(start_time, end_time, time_series):
        total_time = (end_time - start_time).total_seconds() / 60
        active_time = 0
        for timestamp in time_series:
            if start_time.time() <= timestamp.time() <= end_time.time():
                active_time += 1
        
        uptime = active_time
        downtime = total_time - active_time
        
        return uptime, downtime

    # Generate the report
    report_data = []
    for store in business_hours_data:
        store_id = store.store_id
        business_start = datetime.combine(current_time_utc.date(), store.start_time_local)
        business_end = datetime.combine(current_time_utc.date(), store.end_time_local)
        obs_within_business_hours = store_activity_data.filter(
            store_id=store_id,
            timestamp_utc__gte=business_start,
            timestamp_utc__lte=business_end
        ).order_by('timestamp_utc').values('timestamp_utc', 'status')
        
        time_series = extrapolate_time_series(
            obs_within_business_hours,
            business_start,
            business_end
        )
        
        uptime_last_hour, downtime_last_hour = calculate_extrapolated_uptime_downtime(
            last_hour,
            current_time_utc,
            time_series
        )
        
        uptime_last_day, downtime_last_day = calculate_extrapolated_uptime_downtime(
            last_day,
            current_time_utc,
            time_series
        )
        
        uptime_last_week, downtime_last_week = calculate_extrapolated_uptime_downtime(
            last_week,
            current_time_utc,
            time_series
        )
        
        report_data.append({
            'store_id': store_id,
            'uptime_last_hour': uptime_last_hour,
            'uptime_last_day': uptime_last_day,
            'uptime_last_week': uptime_last_week,
            'downtime_last_hour': downtime_last_hour,
            'downtime_last_day': downtime_last_day,
            'downtime_last_week': downtime_last_week,
        })

    return report_data

# Call the generate_report function to generate the report
report = generate_report()

# Print the generated report
for entry in report:
    print(entry)

   # --------------------------------------------------------------------------
    report_csv_file = 'report.csv'
    report_data.to_csv(report_csv_file, index=False)


    ReportStatus.objects.filter(report_id=report_id).update(status=1, end_time=timezone.now())
    
class ImportCsv(APIView):
    def get(self,requst):
        c=Command()
        c.handle_store_status()
        c.handle_store_hours()
        c.handle_store_timezone()
        return Response({'message': 'csv data import started'})
class TriggerReport(APIView):
    def get(self, request):
        report_id = str(uuid.uuid4()) 
        generate_report(report_id)
        return Response({'report_id': report_id})

class GetReport(APIView):
    def post(self, request):
        report_id = request.data.get('report_id')
        report=ReportStatus.objects.filter(report_id=report_id)
        if not len(report):
            return Response({'error': 'invalid report id'}, status=status.HTTP_404_NOT_FOUND)
        if report[0].status ==0 :
             return Response({'message': 'Report generation is Running'}, status=status.HTTP_200_OK)
        try:
            csv = open('dataSource/Menu hours.csv', 'rb')
            response = FileResponse(csv)
            return response
        except FileNotFoundError:
            return Response({'error': 'CSV file not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


