# Remote Backend Django Engineer – AI & Algorithmic Systems Assignment

An API driven backend application designed to optimize long distance vehicle routing by calculating cost effective fueling stops across the USA based on regional pricing metrics, range constraints, and structural spatial corridor analysis algorithms.

---

## 🛠️ Project Phase 1: Data Model & Seed Engine Architecture

This milestone establishes the base database schemas and parses, filters, and processes thousands of target US fuel provider location mappings into a local PostgreSQL database completely offline.

### Key System Dependencies

* **Django & Django REST Framework**: Core API MVC structures.
* **PostgreSQL**: Selected database management system engine.
* **uszipcode**: Fully offline GIS database reference engine used to map addresses to coordinates without external network requests or rate limit penalties.
* **sqlalchemy-mate==2.0.0.0**: Fixed version lock required for absolute compatibility with the `uszipcode` tracking index.

---

## 📁 Core Code Architecture Layout

```text
fuel-api-assignment/
│
├── config/             # Project Configuration Root
│   └── settings.py                     # DB configurations & Core App links
│
├── fuel/                               # Main Feature Application Directory
│   ├── static/                         # Assets Folder
│   │   └── data/
│   │       └── fuel-prices-for-be-assessment.csv
│   │
│   ├── management/                     # Custom Commands Extension Engine
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── import_fuel_stations.py # Optimized sliding window chunk seeder
│   │
│   ├── models.py                       # FuelStation Database Schemas
│   └── views.py                        # Endpoint execution controllers
│
├── manage.py
├── requirements.txt                    # System environment pinning file
└── README.md
```

---

## 💾 Database Schema Representation

### `FuelStation` Model Model Details

The base mapping represents an item matrix optimized for mathematical query sorting operations:

| Field Name       | Type         | Constraints                    | Description                                    |
| :--------------- | :----------- | :----------------------------- | :--------------------------------------------- |
| `id`           | BigAutoField | Primary Key                    | Auto-incrementing identifier.                  |
| `opis_id`      | IntegerField | Unique                         | Structural reference code tracking identity.   |
| `name`         | CharField    | Max length 255                 | Commercial truckstop brand label.              |
| `address`      | CharField    | Max length 255                 | Street line text metadata.                     |
| `city`         | CharField    | Max length 100                 | City name.                                     |
| `state`        | CharField    | Max length 10                  | Target state shorthand identifier.             |
| `rack_id`      | CharField    | Max length 50                  | Internal logistics distribution tracking code. |
| `retail_price` | DecimalField | Max digits 6, 3 decimal places | Cost indicator metric.                         |
| `latitude`     | FloatField   | Required (Non-Nullable)        | Geographic coordinate.                         |
| `longitude`    | FloatField   | Required (Non-Nullable)        | Geographic coordinate.                         |

* **Index Parameters**: Structural lookup fields use fast scanning matrix rules on `state` and `retail_price` attributes to guarantee performance under subsequent corridor mapping loops.

---

## 🚀 Setup & Data Ingestion Instructions

### 1. Environment Configuration

Verify your `requirements.txt` maps explicitly to locked variations, then activate your virtual environment layout and run package installations:

```bash
pip install -r requirements.txt
```

### 2. Connect Your PostgreSQL Database

Verify your administrative parameters inside `fuel_optimizer_project/settings.py` align accurately with your active PostgreSQL or PgAdmin access points:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'postgres',
        'PASSWORD': 'your_secure_password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

### 3. Run System Migrations

Generate initial model schema scripts and execute them against the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Execute the Fast Data Ingestion Command

To populate the database using the self-contained static CSV asset data, execute the memory-safe command:

```bash
python manage.py import_fuel_stations
```

#### Expected Operational Flow Output:

```text
Loading data from: D:\...\fuel\static\data\fuel-prices-for-be-assessment.csv
Pre-loaded 0 existing station IDs into memory.
Flushed 200 total stations to PostgreSQL...
Flushed 400 total stations to PostgreSQL...
...
Successfully finished flushing the remaining stations! Total new records added: 8142
```

---

## 🎯 Upcoming Milestones: Next Project Phase

* **Branch**: `feature/jwt-auth`
* **Objective**: Secure system layers using token authentication tokens via `djangorestframework-simplejwt` components.
