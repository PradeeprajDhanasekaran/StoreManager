# import_csv.py (using pandas with batching)
from datetime import datetime, timezone
from StoreManager.settings import BASE_DIR 
import pandas as pd
from django.core.management.base import BaseCommand
from api.models import StoreStatus , StoreTimezone,StoreHours

class Command(BaseCommand):
    help = 'Import data from CSV file'

    # def add_arguments(self, parser):
    #     parser.add_argument('csv_file', type=str, help='Path to the CSV file')
    #     parser.add_argument('--batch_size', type=int, default=2, help='Batch size for insertion')

    def handle_store_status(self, *args, **kwargs):
        csv_file =BASE_DIR/ 'dataSource/store status.csv'
        batch_size =4000

        df = pd.read_csv(csv_file)
        df['timestamp_utc'] = df['timestamp_utc'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f %Z").replace(tzinfo=timezone.utc))
        total_records = len(df)

        for i in range(0, total_records, batch_size):
            batch_data = df.iloc[i : i + batch_size].to_dict(orient='records')

            StoreStatus.objects.bulk_create([StoreStatus(**item) for item in batch_data])

            self.stdout.write(f'Processed {min(i + batch_size, total_records)} records out of {total_records}')
        self.stdout.write(self.style.SUCCESS('Store status data imported successfully!'))

    def handle_store_hours(self):
        menu_hour_csv =BASE_DIR/ 'dataSource/Menu hours.csv'
        batch_size =4000
        df = pd.read_csv(menu_hour_csv)
        df['start_time_local'] = df['start_time_local'].apply(lambda x: datetime.strptime(x, "%H:%M:%S"))
        df['end_time_local'] = df['end_time_local'].apply(lambda x: datetime.strptime(x, "%H:%M:%S"))
        
        total_records = len(df)
        for i in range(0, total_records, batch_size):
            batch_data = df.iloc[i : i + batch_size].to_dict(orient='records')

            StoreHours.objects.bulk_create([StoreHours(**item) for item in batch_data])

            self.stdout.write(f'Processed {min(i + batch_size, total_records)} records out of {total_records}')
        self.stdout.write(self.style.SUCCESS('Store hours data imported successfully!'))

    def handle_store_timezone(self):
        menu_hour_csv =BASE_DIR/ 'dataSource/timeZones.csv'
        batch_size =4000
        df = pd.read_csv(menu_hour_csv)       
        total_records = len(df)
        for i in range(0, total_records, batch_size):
            batch_data = df.iloc[i : i + batch_size].to_dict(orient='records')

            StoreTimezone.objects.bulk_create([StoreTimezone(**item) for item in batch_data])

            self.stdout.write(f'Processed {min(i + batch_size, total_records)} records out of {total_records}')
        self.stdout.write(self.style.SUCCESS('Timezone data imported successfully!'))
