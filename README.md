
# Voter Analysis Backend
API service for analyzing ward-level voter demographic data in Nepal.

## Project Overview
This Django-based backend facilitates the import, management, and analysis of voter data. It transforms raw CSV data into actionable demographic insights, classifying voters by age, gender, and caste/ethnicity (via surname mapping). Note: This project is strictly a backend service providing a REST API and Admin Interface.

### Key Capabilities
*   **Data Import**: Bulk upload of voter rolls (CSV) with validation.
*   **Demographic Classification**: Automatic categorization of voters:
    *   **Age Groups**: Gen Z (18-29), Working (30-45), Mature (46-60), Senior (60+).
    *   **Caste/Ethnicity**: Inferred from surname using a database of **1200+** mappings (e.g., Kandel -> Brahmin, Thapa -> Chhetri).
*   **Analytics**: Real-time statistical aggregation (Age distributions, Gender ratios, Cross-tabulations).
*   **API**: Fully documented REST API .

---

## Directory Structure
```
backend/
├── backend/                # Project Settings (WSGI, ASGI, URLConf)
├── voters/                 # Main Application
│   ├── models.py           # Database Schema (Voter, SurnameMapping)
│   ├── views.py            # API Endpoints & Logic
│   ├── serializers.py      # JSON Transformation
│   ├── utils/              # Business Logic (Analytics, CSV Processing)
│   └── management/         # Custom Commands (load_surname_mappings)
├── data/                   # Persistent storage (SQLite DB, Uploads)
├── staticfiles/            # Static assets (Django Admin styles)
├── Dockerfile              # Container definition
└── docker-compose.yml      # Orchestration config
```

## Prerequisites
*   **Docker** & **Docker Compose** (Recommended for easiest setup)
*   **Python 3.11+** (If running locally)

---

## Getting Started

### Method 1: Docker (Production-Ready)
This is the preferred method as it isolates dependencies and ensures consistency.

1.  **Build and Start Services**
    ```bash
    sudo docker compose up --build -d
    ```
    The API will be available at `http://localhost:8000`.

3.  **Initialize System** (Run once)
    ```bash
    # Apply database migrations
    sudo docker compose exec web python manage.py migrate

    # Load comprehensive surname-to-caste mappings (1200+ entries)
    sudo docker compose exec web python manage.py load_surname_mappings

    # Create an admin user
    sudo docker compose exec web python manage.py createsuperuser
    ```

4.  **Stop Services**
    ```bash
    sudo docker compose down
    ```
    *(Use `docker compose` with a space for V2, or `docker-compose` for V1)*

### Method 2: Local Development
1.  **Environment Setup**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

2.  **Initialize Database**
    ```bash
    python manage.py migrate
    python manage.py load_surname_mappings
    python manage.py createsuperuser
    ```

3.  **Run Server**
    ```bash
    python manage.py runserver
    ```

---

## Configuration

The application uses environment variables for configuration. In Docker, these are set in `docker-compose.yml`. For production, use a `.env` file.

| Variable | Description | Default |
| :--- | :--- | :--- |
| `DEBUG` | Toggle debug mode (True/False) | `True` |
| `SECRET_KEY` | Django security key | *(Default dev key)* |
| `ALLOWED_HOSTS` | Comma-separated allowlist | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS`| Frontend URLs for CORS | `http://localhost:3000` |

---

### API Endpoints with Examples

#### Public Endpoints (No Authentication Required)

##### 1. **GET /api/voters/** - List/Search Voters
Returns paginated list of voters with support for filtering and searching.

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Results per page (default: 50, max: 200)
- `age_min`, `age_max` - Age range filter
- `age_group` - Filter by age category (`gen_z`, `working`, `mature`, `senior`)
- `gender` - Filter by gender (`male`, `female`, `other`)
- `caste_group` - Filter by caste group
- `ward` - Filter by ward number
- `search` - Search in voter names

**Example Request:**
```bash
# Get all voters
curl http://localhost:8000/api/voters/

# Filter: age 25-40, ward 5
curl "http://localhost:8000/api/voters/?age_min=25&age_max=40&ward=5"
```

**What you will get:**
- `count`: Total number of voters matching filters.
- `next/previous`: Links to next/previous pages.
- `results`: Array of voter objects containing:
  - `voter_id`: Unique identifier from voter roll.
  - `name`: Full name of voter.
  - `age`: Age in years.
  - `age_group`: Category (e.g., "working").
  - `gender`: male/female/other.
  - `ward`: Ward number.
  - `caste_group`: Inferred ethnicity (e.g., "brahmin").

**Example Response:**
```json
{
  "count": 250,
  "next": "http://localhost:8000/api/voters/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "voter_id": "V12345",
      "name": "Ram Kumar Sharma",
      "age": 32,
      "age_group": "working",
      "gender": "male",
      "ward": 5,
      "caste_group": "brahmin"
    }
  ]
}
```

---

##### 2. **GET /api/analysis/overview/** - Demographic Overview
Returns comprehensive demographic statistics for all voters (or filtered subset).

**Example Request:**
```bash
curl http://localhost:8000/api/analysis/overview/
```

**What you will get:**
- `total_voters`: Total count in the selection.
- `average_age`: Arithmetic mean of ages.
- `median_age`: Middle value of ages.
- `gender_distribution`: Object with counts per gender.
- `age_group_summary`: Object with counts per age category.
- `caste_summary`: Object with counts per caste group.

**Example Response:**
```json
{
  "total_voters": 2450,
  "average_age": 42.5,
  "median_age": 40,
  "gender_distribution": { "male": 1250, "female": 1180, "other": 20 },
  "age_group_summary": { "gen_z": 580, "working": 920, "mature": 680, "senior": 270 },
  "caste_summary": { "brahmin": 520, "chhetri": 680, "janajati": 550, ... }
}
```

---

##### 3. **GET /api/analysis/age-distribution/** - Age Distribution
Returns age group data specifically formatted for chart libraries.

**Example Request:**
```bash
curl http://localhost:8000/api/analysis/age-distribution/
```

**What you will get:**
- `chart_data`:
  - `labels`: Human-readable category names.
  - `values`: Raw counts for each category.
  - `percentages`: Percentage of total for each category.
- `total`: Total voters analyzed.

**Example Response:**
```json
{
  "chart_data": {
    "labels": ["Gen Z (18-29)", "Working (30-45)", "Mature (46-60)", "Senior (60+)"],
    "values": [580, 920, 680, 270],
    "percentages": [23.7, 37.6, 27.8, 11.0]
  },
  "total": 2450
}
```

---

#### Admin & Management Endpoints (Bypassed CSRF for Frontend Integration)

##### 4. **POST /api/admin/upload/** - Upload CSV File
Processes a CSV file and returns import statistics.

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/admin/upload/ -F "file=@voters.csv"
```
> [!NOTE]
> Authentication is currently relaxed for this endpoint to facilitate frontend testing.

**What you will get:**
- `success`: Boolean status.
- `total`: Total rows found in CSV.
- `imported`: Successfully saved records.
- `failed`: Records skipped due to errors.
- `unmapped_surnames`: List of surnames found that have no caste mapping (useful for admin review).
- `processing_time`: Seconds taken to process.

**Example Response:**
```json
{
  "success": true,
  "total": 500,
  "imported": 485,
  "failed": 15,
  "unmapped_surnames": ["Xyz", "Unknown"],
  "processing_time": 2.35
}
```

---

##### 5. **GET /api/admin/upload-history/** - Upload History
List of past CSV processing jobs.

**What you will get:**
- `results`: List of jobs containing:
  - `file_name`: Original name of uploaded file.
  - `status`: completed/failed.
  - `successful_imports/failed_imports`: Specific counts for that job.
  - `uploaded_at`: Timestamp.

**Example Response:**
```json
{
  "results": [
    {
      "file_name": "voters_ward5.csv",
      "total_records": 500,
      "successful_imports": 485,
      "status": "completed"
    }
  ]
}
```

---

##### 6. **GET /api/admin/surnames/** - Surname Mappings
Manage the database used to infer caste from surnames.

**Example Request:**
```bash
# Add new mapping
curl -X POST http://localhost:8000/api/admin/surnames/ \
  -H "Content-Type: application/json" -d '{"surname": "Sharma", "caste_group": "brahmin"}'
```

**Upsert Behavior**:
If a surname already exists in the database, a `POST` request will **update** the existing record instead of returning secondary errors. This allows for seamless batch loading from the frontend.

**What you will get:**
- `surname`: The family name.
- `caste_group`: The category it maps to.

**Example Response:**
```json
{
  "id": 1,
  "surname": "Sharma",
  "caste_group": "brahmin"
}
```


---

## Troubleshooting

### Port Conflicts
**Error**: `Error: That port is already in use.`
**Solution**: verify no other service is using port 8000.
*   **Docker**: Change the port mapping in `docker-compose.yml` (e.g., `"8080:8000"`).
*   **Local**: Run on a different port: `python manage.py runserver 8081`.

### Database Persistence
In Docker, database files (`db.sqlite3`) and uploaded files are persisted in the `./data` directory on your host machine. Do not delete this folder unless you intend to reset the data.

### Missing Caste Data
If voters appear as "Unknown" caste:
1.  Check `api/admin/surnames/` to see if the surname is mapped.
2.  Add a new mapping via the Admin Panel or API.
3.  Re-process the upload or update the record.
>>>>>>> b549d45 (vote classifier done)
