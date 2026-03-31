# Quick Start Guide

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Step 1: Install Dependencies

Run from the project directory:

```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database

A helper SQL script (`db/init_db.sql`) is provided for PostgreSQL – it
creates the `horse_races` database, a `horse_races_admin` user, and
all of the tables.  Make sure you have `psql` installed and run:

```bash
psql -U postgres -f db/init_db.sql
```

If the database already exists, drop it first:
```bash
psql -U postgres -c "DROP DATABASE horse_races;"
psql -U postgres -f db/init_db.sql
```

The application configuration (in `config.py`) defaults to use the
`horse_races_admin` account; you can override the connection string by
setting `DATABASE_URL`.

If you do not have PostgreSQL available, the project will fall back to
SQLite: simply running the app will create a local
`horse_races.db` with the required schema.

To explicitly create the database via the Python code (for either
backend) run:

```bash
python app.py
```

That command will:
1. Connect to the configured database (Postgres or SQLite)
2. Create any missing tables
3. Start the Flask development server

### Step 3: Access the Application

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### Step 4 (Optional): Load Sample Data

To populate the database with sample data for testing:

```bash
python init_data.py
```

This will create:
- 4 horse owners
- 8 horses with ratings
- 6 jockeys with ratings
- 3 sample races (2 finished, 1 scheduled)

## 📚 Features & How to Use

### 1. **Manage Horse Owners**
   - Navigate to the "Owners" tab
   - Click "Add Owner" to register a new owner
   - Each owner can have multiple horses

### 2. **Manage Horses**
   - Go to "Horses" tab
   - Click "Add Horse" to register a new horse
   - Select an owner and set an initial rating
   - View all horses and their owners

### 3. **Manage Jockeys**
   - Go to "Jockeys" tab
   - Click "Add Jockey" to register a new jockey
   - Set an initial rating for the jockey
   - View all jockeys and their statistics

### 4. **Organize Races**
   - Click "New Race" or go to "Races" → "New Race"
   - Select date and time
   - Add horse-jockey pairs as race participants
   - Add up to 10 participants per race (click "Add More Participants")
   - Create the race

### 5. **Record Race Results**
   - Go to "Races" and select a race
   - Click "Edit Results"
   - Enter placement numbers (1st, 2nd, 3rd, etc.)
   - Save results to update race status

## 🗄️ Database Schema

The application uses **SQLAlchemy** ORM with Alembic for migrations.

**Tables:**
- `owners` - Horse owners
- `horses` - Racehorses (many-to-one with owners)
- `jockeys` - Jockeys
- `races` - Race events
- `race_entries` - Participants (many-to-many: horse + jockey per race)

## 🔧 Using Alembic for Database Changes

If you modify the models in `models.py`, create a migration:

```bash
# Generate migration (auto-detects changes)
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback to previous version
flask db downgrade
```

## 📁 Project Structure

```
app/
├── app.py                    # Main Flask application with routes
├── models.py                 # SQLAlchemy database models
├── config.py                 # Configuration (DB URI, secret key, etc.)
├── requirements.txt          # Python dependencies
├── init_data.py              # Optional sample data generator
├── alembic.ini              # Alembic configuration
├── migrations/              # Database migrations
│   ├── env.py               # Alembic setup
│   ├── script.py.mako       # Migration template
│   └── versions/            # Migration scripts
│       └── 001_initial.py   # Initial schema migration
└── templates/               # Jinja2 HTML templates
    ├── base.html            # Base template
    ├── index.html, races.html, race_detail.html
    ├── horses.html, add_horse.html
    ├── jockeys.html, add_jockey.html
    ├── owners.html, add_owner.html
    ├── edit_race_results.html
    └── 404.html, 500.html   # Error pages
```

## ⚙️ Configuration

Edit `config.py` (or set environment variables) to change the
connection details:

- *Database URL*: `SQLALCHEMY_DATABASE_URI` (constructed from the
  following individual variables unless you override with
  `DATABASE_URL`)
  - `DB_USER` (default: `horse_races_admin`)
  - `DB_PASS` (empty by default)
  - `DB_HOST` (default: `localhost`)
  - `DB_PORT` (default: `5432`)
  - `DB_NAME` (default: `horse_races`)

You can still point the app at a local SQLite file by setting the URL
explicitly:
```
export DATABASE_URL=sqlite:///horse_races.db
```
  
- **Secret Key**: `SECRET_KEY` (change for production!)

- **Session Timeout**: `PERMANENT_SESSION_LIFETIME`

## 🐛 Troubleshooting

### Database Issues
If the database gets corrupted, delete `horse_races.db` and restart:
```bash
rm horse_races.db
python app.py
```

### Module Not Found Errors
Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### Port Already in Use
If port 5000 is in use, modify `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change port here
```

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop and mobile
- **Color-Coded Status**: Races show Scheduled, In Progress, or Finished
- **Dynamic Forms**: Add/remove race participants with JavaScript
- **Flash Messages**: Get feedback on actions (success/error)
- **Beautiful Styling**: Modern gradient background and card layouts
- **Navigation**: Easy access to all features via top menu and buttons

## 📦 Technologies Used

- **Flask** - Web framework
- **SQLAlchemy** - ORM (Object-Relational Mapping)
- **Alembic** - Database migrations
- **Jinja2** - Template engine
- **SQLite/PostgreSQL/MySQL** - Database options

## 💡 Example Usage

1. **Create an owner**: Go to Owners → Add Owner → Enter "John Smith"
2. **Add a horse**: Go to Horses → Add Horse → Select owner → Enter "Thunder", rating 8.5
3. **Add a jockey**: Go to Jockeys → Add Jockey → Enter "James Lewis", rating 8.7
4. **Create a race**: Click New Race → Select date → Add "Thunder" with "James Lewis" → Create
5. **Record results**: Go to race → Edit Results → Enter "1" for Thunder-Lewis → Save

## 📞 Notes

- All horse and jockey names must be **unique**
- Same horse-jockey pair cannot be added twice to the same race
- Ratings range from 0 to 10
- Placements are optional until you edit race results
- The UI uses Jinja2 templates (not JSON API)

## 🚀 Deployment

For production deployment:

1. Change `SECRET_KEY` in `config.py`
2. Set `debug=False` in `app.py`
3. Use a production WSGI server (Gunicorn, uWSGI)
4. Use PostgreSQL or MySQL instead of SQLite
5. Set environment variables for sensitive data

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

---

Enjoy managing your horse races! 🐴🏁
