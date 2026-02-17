# Voter Analysis Backend

A Django-based backend for processing and analyzing hierarchical voter data in Nepal.

#### **Step 1: Start the System**
```bash
sudo docker compose up --build -d
```

#### **Step 2: Initialize Database and Mappings**
Run these commands once to set up the system.
```bash
# 1. Create database tables
sudo docker compose exec web python manage.py migrate

# 2. Load surname-to-caste mappings (Critical for demographic analysis)
sudo docker compose exec web python manage.py load_surname_mappings

# 3. Create an admin user (for logging in to /admin)
sudo docker compose exec web python manage.py createsuperuser
```

---

## 📂 Data Import Procedures

### **Option A: Importing Large Datasets (CLI Method)**
**Best for:** Bulk imports, large files, avoiding timeouts.

**1. Place Data in the Correct Location**
All your CSV folders must be inside the project's `backend/data/` directory.

> **Path Mapping:** 
> *   Current Location: `backend/data/YourFolder`
> *   Docker Location: `/app/data/YourFolder`

**2. Choose Your Import Method**

#### **Scenario 1: Import a Single Province**
Structure: `backend/data/GandakiProvince/` (containing CSVs for constituencies)

**Command:**
```bash
# Syntax: import_voter_data /app/data/<Folder_Name>
sudo docker compose exec web python manage.py import_voter_data /app/data/GandakiProvince
```

#### **Scenario 2: Bulk Import (Multiple Provinces)**
Structure: `backend/data/AllProvinces/` (containing `Gandaki`, `Bagamati`, etc.)

**Command:**
```bash
sudo docker compose exec web python manage.py import_voter_data /app/data/AllProvinces
```

**3. Verify**
You will see a summary of files processed and records imported in the terminal.


---

## 📊 API Usage

### **Analysis Endpoints**
Get demographic breakdowns filtered by hierarchy.

- **Overview**: `GET /api/analysis/overview/`
- **Age Distribution**: `GET /api/analysis/age-distribution/`
- **Caste Distribution**: `GET /api/analysis/caste-distribution/`

**Filters:**
You can filter any analysis endpoint by:
- `province` (e.g., `?province=Bagamati`)
- `constituency` (e.g., `?constituency=Kathmandu-1`)
- `district`
- `ward`

### **Voter Search**
Search for individual voters.
- `GET /api/voters/?search=Ram&constituency=Kathmandu-1`

---

## 📖 API Endpoint Examples

> [!IMPORTANT]
> **Data Language Format**
> Please note the specific language requirements for different fields based on the source data:
> - **Nepali (Devanagari)**: Name (`name`), Province (`province`), District (`district`), Municipality (`municipality`).
> - **English / Numbers**: Constituency (`constituency`), Ward (`ward`), Age (`age`), Voter ID (`voter_id`).
> 
> *Example:* Searching for a voter in "Kaski" district must use `?district=कास्की`.

### 1. Analysis Endpoints (Public)

#### **Overview Statistics**
Get total counts broken down by demographics.
- **Endpoint**: `GET /api/analysis/overview/`
- **Parameters**: `province`, `district`, `constituency`, `ward`, `age_min`, `age_max`, `gender`, `caste_group`

**Request:**
```bash
# Get stats for Gandaki Province (using Nepali name)
curl "http://localhost:8000/api/analysis/overview/?province=गण्डकी"

# Get stats for Baglung District (Nepali), Constituency 1 (English)
curl "http://localhost:8000/api/analysis/overview/?district=बाग्लुङ&constituency=Baglung-1"
```

**Response:**
```json
{
  "total_voters": 150000,
  "average_age": 42.5,
  "gender_distribution": { "male": 76000, "female": 74000 },
  "caste_group_distribution": { "Brahmin": 45000, "Chhetri": 40000 },
  "age_group_distribution": { "gen_z": 30000, "working": 60000 }
}
```

#### **Age Distribution**
Get age groups for charts.
- **Endpoint**: `GET /api/analysis/age-distribution/`

**Request:**
```bash
# Get age distribution for Ward 4 in Baglung
curl "http://localhost:8000/api/analysis/age-distribution/?district=बाग्लुङ&ward=4"
```

**Response:**
```json
{
  "labels": ["18-25", "26-40", "41-60", "60+"],
  "data": [1500, 4500, 3000, 1000]
}
```

---

### 2. Voter Data Endpoints (Public)

#### **List & Search Voters**
- **Endpoint**: `GET /api/voters/`
- **Parameters**: `search` (name/voter_id), `province`, `district`, `constituency`

**Request:**
```bash
# Search by Name in Nepali
curl "http://localhost:8000/api/voters/?search=बहादुर"

# Filter by District (Nepali) and Ward (Number)
curl "http://localhost:8000/api/voters/?district=बाग्लुङ&ward=4"
```

**Response:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "voter_id": 12345678,
      "name": "डन बहादुर थापा",
      "age": 43,
      "province": "GandakiProvince",
      "district": "बाग्लुङ",
      "constituency": "Baglung-1",
      "municipality": "Baglung",
      "ward": 4
    }
  ]
}
```

#### **Get Single Voter**
- **Endpoint**: `GET /api/voters/{id}/`

**Request:**
```bash
curl "http://localhost:8000/api/voters/12345678/"
```

---

### 3. Admin Endpoints

#### **Upload History**
Check status of past uploads.
- **Endpoint**: `GET /api/admin/upload-history/`

**Request:**
```bash
curl "http://localhost:8000/api/admin/upload-history/"
```

**Response:**
```json
[
  {
    "id": 1,
    "file_name": "Gandaki_Kaski.csv",
    "uploaded_at": "2023-10-27T10:00:00Z",
    "status": "completed",
    "total_records": 5000,
    "success_count": 5000,
    "error_count": 0
  }
]
```

#### **Surname Mappings (Manage Castes)**
Manage how surnames are mapped to caste groups.

> **Note:** Surnames are stored in **Nepali**. You must search using Nepali text (e.g., `थापा`) unless an English mapping explicitly exists.

- **List/Search**: `GET /api/admin/surnames/?search=Thinking`
- **Create**: `POST /api/admin/surnames/`
- **Update**: `PUT /api/admin/surnames/{id}/`
- **Delete**: `DELETE /api/admin/surnames/{id}/`

**Examples:**

1. **Search (Nepali)**:
   ```bash
   curl "http://localhost:8000/api/admin/surnames/?search=थापा"
   ```
   *Response:*
   ```json
   [
     { "id": 15, "surname": "थापा", "caste_group": "chhetri" }
   ]
   ```

2. **Add New Mapping (English)**:
   ```bash
   curl -X POST http://localhost:8000/api/admin/surnames/ \
     -H "Content-Type: application/json" \
     -d '{"surname": "Thapa", "caste_group": "chhetri"}'
   ```

#### **Upload Data (CSV)**

- **Upload CSV**:
  ```bash
  curl -X POST http://localhost:8000/api/admin/upload/ \
    -F "file=@/path/to/data.csv"
  ```

## 🛠️ Access Points

- **API Root**: [http://localhost:8000/api/](http://localhost:8000/api/)
- **Admin Panel**: [http://localhost:8000/admin/](http://localhost:8000/admin/) (Login with the superuser created in Step 2)

---

## 🐞 Troubleshooting

**"Folder does not exist" Error**:
Ensure you placed your data folder inside `backend/data/` on your host machine, and are referencing it as `/app/data/...` in the command.

**"Permission Denied"**:
Always use `sudo` with `docker compose` commands if you are not in the docker group.
