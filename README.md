
# Remote Backend Django Engineer – AI & Algorithmic Systems Assignment

An API driven backend application designed to optimize long distance vehicle routing by calculating cost effective fueling stops across the USA based on regional pricing metrics, range constraints, and structural spatial corridor analysis algorithms.

---

## Project Phase 1: Data Model & Seed Engine Architecture

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
│   ├── services/                       # Algorithmic & Spatial Helper Layer
│   │   ├── __init__.py
│   │   ├── ai.py                       # Spatial spatial cluster interface
│   │   └── router.py                   # Core route evaluation paths
│   └── views.py                        # Endpoint execution controllers
│
├── manage.py
├── requirements.txt                    # System environment pinning file
└── README.md
```

---

## Database Schema Representation

### `FuelStation` Model Details

The base mapping represents an item matrix optimized for mathematical query sorting operations:

| Field Name       | Type         | Constraints                    | Description                                    |
| :--------------- | :----------- | :----------------------------- | :--------------------------------------------- |
| `id`           | BigAutoField | Primary Key                    | Auto incrementing identifier.                  |
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

Verify your administrative parameters inside `config/settings.py` align accurately with your active PostgreSQL or PgAdmin access points:

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

To populate the database using the self contained static CSV asset data, execute the memory safe command:

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

## API Core Endpoints Specification

The application routes traffic through a unified spatial processing controller layer.

### 1. User Registration Profile

* **Endpoint**: `POST /api/auth/register/`
* **Payload Structure**:

  ```json
  {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "your_secure_password"
  }
  ```
* **Success Response (`201 Created`)**: Confirms user instantiation parameters.

### 2. Route Optimization Core Matrix

* **Endpoint**: `POST /api/optimize-route/`
* **Payload Structure**:
  ```json
  {
    "start_location": "Los Angeles, CA",
    "destination_location": "New York, NY",
    "route_type": "car"
  }
  ```
* **Algorithmic Logic Layout**:
  * Resolves source and target coordinates via the Nominatim geocoding gateway.
  * Streams structural path segments through the Open Source Routing Machine (OSRM) engine.
  * Extracts proximal candidate stops utilizing `ai_spatial_assistant` vector spatial clustering interfaces.
  * Filters and isolates efficient fueling nodes based on a strict 500 mile vehicle tank range limit at a 10 MPG structural threshold.
  * Approach is Greedy and sampling (not process each corordinate in the route).
* **Success Response (`200 OK`)**:
  ```json
  {
      "summary": {
          "start": "New York, NY",
          "finish": "Los Angeles, CA",
          "start_coords": [
              40.7127281,
              -74.0060152
          ],
          "finish_coords": [
              34.0536909,
              -118.242766
          ],
          "total_distance_miles": 2798.19,
          "total_fuel_cost_usd": 785.91,
          "fuel_efficiency": "10 MPG",
          "max_tank_range": "500 miles"
      },
      "optimal_fuel_stops": [
          {
              "opis_id": 63516,
              "name": "SHEETZ #701",
              "address": "I-81, EXIT 273, Mount Jackson, VA",
              "retail_price": 2.874,
              "mile_marker": 263.15,
              "latitude": 38.74,
              "longitude": -78.63
          },
     ]
  }
  ```

```
Note: You can see the sample output from fuel/static/data/greedy_response.json
```

🎯 Upcoming Milestones: Next Project Phase

* **Branch**: **`fix/fuel-route-optimization`**
  **Objective**: Refactor the optimization engine to replace the local-minimum greedy look-ahead selection script with a global Monotonic Sliding-Window Dynamic Programming matrix.
  **Performance Matrix Targets**:
  * Reduce algorithmic complexity from standard backward induction $O(N^2)$ down to true linear time $O(N)$ using stateful double-ended queue wrappers (**`collections.deque`**).
  * Integrate absolute floating-point preservation tracking blocks via native **`Decimal`** data type encapsulation.
