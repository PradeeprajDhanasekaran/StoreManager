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

    stores = StoreHours.objects.all()
    store_status_data = StoreStatus.objects.all()

    # Initialize an empty DataFrame to store the report data
    report_data = pd.DataFrame(columns=['store_id', 'uptime_last_hour', 'uptime_last_day', 'uptime_last_week', 'downtime_last_hour', 'downtime_last_day', 'downtime_last_week'])

    # Implement the logic to compute uptime and downtime for each store based on the provided data
    for store in stores:
        store_id = store.store_id

        # Get the business hours for the store
        business_hours = (store.start_time_local, store.end_time_local)

        # Filter the status data for the current store
        store_status_data_filtered = store_status_data.filter(store_id=store_id)

        # Calculate uptime and downtime based on the provided data
        ...

        # Extrapolate the data to cover the entire time interval (e.g., last hour, last day, last week)
        ...

        # Store the computed results in the report_data DataFrame
        report_data = report_data.append({
            'store_id': store_id,
            'uptime_last_hour': uptime_last_hour,
            'uptime_last_day': uptime_last_day,
            'uptime_last_week': uptime_last_week,
            'downtime_last_hour': downtime_last_hour,
            'downtime_last_day': downtime_last_day,
            'downtime_last_week': downtime_last_week,
        }, ignore_index=True)

    # You now have the report data in the report_data DataFrame

    # Convert the report_data DataFrame to a CSV file and save it locally
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


