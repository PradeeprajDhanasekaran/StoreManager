# import_csv.py (using pandas with batching)
from datetime import datetime, timezone

import pandas as pd
from django.core.management.base import BaseCommand
from api.models import StoreStatus

class Command(BaseCommand):
    help = 'Import data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('--batch_size', type=int, default=2, help='Batch size for insertion')

    def handle(self, *args, **kwargs):
        csv_file = '/home/softsuave/Desktop/StoreManager/dataSource/storestatus.csv'
        batch_size = kwargs['batch_size']

        # Use Pandas to read the CSV file and convert it into a DataFrame
        df = pd.read_csv(csv_file)
        df['timestamp_utc'] = df['timestamp_utc'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f %Z").replace(tzinfo=timezone.utc))
        # Get the total number of records
        total_records = len(df)

        # Use batching for data insertion
        for i in range(0, total_records, batch_size):
            batch_data = df.iloc[i : i + batch_size].to_dict(orient='records')

            # Use Django's bulk_create() to insert data into the database for each batch
            StoreStatus.objects.bulk_create([StoreStatus(**item) for item in batch_data])

            # Print progress
            self.stdout.write(f'Processed {min(i + batch_size, total_records)} records out of {total_records}')

        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
