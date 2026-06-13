import csv
from pathlib import Path


class FuelPriceLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.prices = []

    def load(self):
        data = []

        with open(self.file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    data.append({
                        'id': row['OPIS Truckstop ID'],
                        'name': row['Truckstop Name'],
                        'address': row['Address'],
                        'city': row['City'],
                        'state': row['State'],
                        'rack_id': row['Rack ID'],
                        'price': float(row['Retail Price'])
                    })
                except (ValueError, KeyError):
                    continue

        self.prices = data
        return data

    def get_all(self):
        return self.prices