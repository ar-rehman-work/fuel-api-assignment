from django.core.management.base import BaseCommand
from django.contrib.staticfiles import finders
from fuel.models import FuelStation
from uszipcode import SearchEngine
from decimal import Decimal
import csv

class Command(BaseCommand):
    help = 'Imports fuel stations from a CSV file optimized with in-memory pre-fetching.'

    def handle(self, *args, **options):
        csv_file_path = finders.find('data/fuel-prices-for-be-assessment.csv')
        
        if not csv_file_path:
            self.stdout.write(self.style.ERROR("Could not locate 'data/fuel-prices-for-be-assessment.csv' inside any static folder."))
            return

        self.stdout.write(f"Loading data from: {csv_file_path}")

        stations_to_create = []

        search = SearchEngine(simple_or_comprehensive=SearchEngine.SimpleOrComprehensiveArgEnum.simple)

        existing_ids = set(FuelStation.objects.values_list('opis_id', flat=True))
        self.stdout.write(f"Pre-loaded {len(existing_ids)} existing station IDs into memory.")

        BATCH_SIZE = 500
        total_inserted = 0

        with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    opis_id = int(row.get('OPIS Truckstop ID').strip())
                except (ValueError, TypeError):
                    continue

                if opis_id in existing_ids:
                    continue

                name = row.get('Truckstop Name').strip()
                address = row.get('Address').strip()
                city = row.get('City').strip()
                state = row.get('State').strip()
                rack_id = row.get('Rack ID').strip()
                
                raw_price = row.get('Retail Price').strip()
                if not raw_price:
                    continue
                retail_price = Decimal(str(raw_price).replace('$', '').strip())

                latitude, longitude = None, None
                try:
                    results = search.by_city_and_state(city=city, state=state)
                    if results and len(results) > 0:
                        first_match = results[0]
                        latitude = first_match.lat
                        longitude = first_match.lng
                except Exception:
                    pass

                if latitude is None or longitude is None:
                    continue

                stations_to_create.append(
                    FuelStation(
                        opis_id=opis_id,
                        name=name,
                        address=address,
                        city=city,
                        state=state,
                        rack_id=rack_id,
                        retail_price=retail_price,
                        latitude=latitude,
                        longitude=longitude
                    )
                )
                
                existing_ids.add(opis_id)
                
                if len(stations_to_create) >= BATCH_SIZE:
                    FuelStation.objects.bulk_create(stations_to_create)
                    total_inserted += len(stations_to_create)
                    self.stdout.write(f"Flushed {total_inserted} total stations to PostgreSQL...")
                    stations_to_create.clear()

        if stations_to_create:
            remaining_count = len(stations_to_create)
            FuelStation.objects.bulk_create(stations_to_create)
            total_inserted += remaining_count
            self.stdout.write(self.style.SUCCESS(f"Successfully finished flushing the remaining {remaining_count} stations! Total new records added: {total_inserted}"))
        else:
            if total_inserted > 0:
                self.stdout.write(self.style.SUCCESS(f"Successfully imported a total of {total_inserted} fuel stations!"))
            else:
                self.stdout.write(self.style.WARNING('No new fuel stations found to insert.'))
