from django.http import FileResponse, HttpResponse
import pandas as pd
from datetime import timedelta
from .models import StoreStatus, StoreHours, StoreTimezone
from .serializers import StoreStatusSerializer, StoreHoursSerializer
from rest_framework.views import APIView,Response
from rest_framework.decorators import api_view
from rest_framework import status
import uuid
from StoreManager.settings import BASE_DIR
def generate_report():
    # Retrieve data from the database for each store
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
        # ...

        # Extrapolate the data to cover the entire time interval (e.g., last hour, last day, last week)
        # ...

        # Store the computed results in the report_data DataFrame
        # report_data = report_data.append({
        #     'store_id': store_id,
        #     'uptime_last_hour': uptime_last_hour,
        #     'uptime_last_day': uptime_last_day,
        #     'uptime_last_week': uptime_last_week,
        #     'downtime_last_hour': downtime_last_hour,
        #     'downtime_last_day': downtime_last_day,
        #     'downtime_last_week': downtime_last_week,
        # }, ignore_index=True)

    # You now have the report data in the report_data DataFrame

    # Convert the report_data DataFrame to a CSV file and save it locally
    # report_csv_file = 'report.csv'
    # report_data.to_csv(report_csv_file, index=False)

    # # Upload the report to Amazon S3
    # bucket_name = 'your_s3_bucket_name'
    # s3_file_key = 'path/to/report.csv'

    # try:
    #     s3_client = boto3.client('s3')
    #     s3_client.upload_file(report_csv_file, bucket_name, s3_file_key)

    #     # Optionally, you can set the access control of the object if needed
    #     s3_client.put_object_acl(ACL='public-read', Bucket=bucket_name, Key=s3_file_key)

    # except ClientError as e:
    #     print("Error uploading report to S3:", e)

    # # Delete the local report file
    # os.remove(report_csv_file)

    # # Return the S3 file URL for future retrieval
    # s3_file_url = f'https://{bucket_name}.s3.amazonaws.com/{s3_file_key}'
    # return s3_file_url
class TriggerReport(APIView):
    def get(self, request):
        report_id = str(uuid.uuid4())  # Generate a random report_id
        # Code to trigger report generation and store report_id for later retrieval
        # ...

        return Response({'report_id': report_id})

class GetReport(APIView):
    def get(self, request):
        report_id = request.GET.get('report_id')

        # Check if the report is generated or still running
        # ...

        # If report generation is complete, return the CSV file
        # ...

        # If report generation is still running, return "Running"
        try:
            csv = open('dataSource/Menu hours.csv', 'rb')
            response = FileResponse(csv)
            return response
        except FileNotFoundError:
            return Response({'error': 'CSV file not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response("Running")


