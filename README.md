# Task Manager — Full Stack App
> React + Python Flask + MySQL

---

## Project Structure

```
taskmanager/
├── backend/
│   ├── app.py            ← Flask REST API
│   ├── schema.sql        ← MySQL database setup
│   └── requirements.txt  ← Python dependencies
└── frontend/
    └── index.html        ← React app (no build needed!)
```

---

## Step 1 — Set Up MySQL (MySQL Workbench)

1. Open **MySQL Workbench**
2. Connect to your local server
3. Open `backend/schema.sql`
4. Click ▶ **Run** (or press Ctrl+Shift+Enter)

This creates the `taskmanager` database and `tasks` table.

---

## Step 2 — Configure Database Password

Open `backend/app.py` and update:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",        # your MySQL username
    "password": "root",    # your MySQL password
    "database": "taskmanager"
}
```

---

## Step 3 — Run the Flask Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Flask runs on → http://localhost:5000

---

## Step 4 — Open the Frontend

Just open `frontend/index.html` in your browser.
No npm, no build step — React loads from CDN!

---

## API Endpoints

| Method | Endpoint          | Action            |
|--------|-------------------|-------------------|
| GET    | /tasks            | Get all tasks     |
| POST   | /tasks            | Create a task     |
| PUT    | /tasks/<id>       | Toggle status     |
| DELETE | /tasks/<id>       | Delete a task     |

---

## Tech Stack

- **Frontend**: React 18 (CDN), Babel standalone
- **Backend**: Python Flask + Flask-CORS
- **Database**: MySQL via mysql-connector-python
