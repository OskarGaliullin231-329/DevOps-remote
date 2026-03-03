# Horse Racing Management System

Flask application for organizing and managing horse races with a database backend, ORM (SQLAlchemy), and automatic migrations (Alembic).

## Features

- **Horse Management**: Add and manage horses with ratings and owners
- **Owner Management**: Register horse owners
- **Jockey Management**: Add and manage jockeys with ratings
- **Race Management**: Create races, assign horses and jockeys to races, and record race results
- **Results Tracking**: Record placements and view race outcomes
- **Web Interface**: Clean, responsive Jinja2 templated UI

## Database Schema

### Tables

1. **owners**
   - `id` (Integer, Primary Key)
   - `name` (String, Unique)

2. **horses**
   - `id` (Integer, Primary Key)
   - `name` (String, Unique)
   - `rating` (Float)
   - `owner_id` (Foreign Key to owners)

3. **jockeys**
   - `id` (Integer, Primary Key)
   - `name` (String, Unique)
   - `rating` (Float)

4. **races**
   - `id` (Integer, Primary Key)
   - `date` (DateTime)

5. **race_entries** (Many-to-Many: Race ↔ Jockey ↔ Horse)
   - `id` (Integer, Primary Key)
   - `race_id` (Foreign Key to races)
   - `jockey_id` (Foreign Key to jockeys)
   - `horse_id` (Foreign Key to horses)
   - `place` (Integer, nullable - placement in the race)
   - **Unique Constraint**: (race_id, jockey_id, horse_id)

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize the Database

The application uses Alembic for database migrations. To set up the database:

```bash
# Create the database and run migrations
flask db upgrade

# Or manually run the app (will create db.sqlite if needed)
python app.py
```

### 3. Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

## Using Alembic for Migrations

### Creating a New Migration

If you modify the models, create a migration with:

```bash
flask db migrate -m "Description of changes"
```

### Applying Migrations

```bash
flask db upgrade
```

### Downgrading to Previous Version

```bash
flask db downgrade
```

### Viewing Migration History

```bash
flask db history
```

## Project Structure

```
app/
├── app.py                    # Main Flask application
├── models.py                 # SQLAlchemy models
├── config.py                 # Configuration
├── requirements.txt          # Python dependencies
├── alembic.ini              # Alembic configuration
├── alembic/
│   ├── env.py               # Alembic environment setup
│   ├── script.py.mako       # Migration template
│   └── versions/
│       └── 001_initial.py   # Initial migration
└── templates/               # Jinja2 templates
    ├── base.html            # Base template
    ├── index.html           # Home page
    ├── horses.html          # Horses list
    ├── add_horse.html       # Add horse form
    ├── jockeys.html         # Jockeys list
    ├── add_jockey.html      # Add jockey form
    ├── owners.html          # Owners list
    ├── add_owner.html       # Add owner form
    ├── races.html           # Races list
    ├── add_race.html        # Create race form
    ├── race_detail.html     # Race details
    ├── edit_race_results.html # Edit race placements
    ├── 404.html             # 404 error page
    └── 500.html             # 500 error page
```

## Usage Examples

### 1. Add an Owner

Navigate to "Owners" → "Add Owner" and enter the owner's name.

### 2. Add a Horse

1. Go to "Horses" → "Add Horse"
2. Select an owner
3. Enter horse name and rating

### 3. Add a Jockey

Navigate to "Jockeys" → "Add Jockey" and enter the jockey's name and rating.

### 4. Create a Race

1. Go to "New Race"
2. Select a date/time
3. Add horse-jockey pairs as participants
4. Create the race

### 5. Record Race Results

1. View a race from "Races"
2. Click "Edit Results"
3. Enter the placement number for each participant
4. Save results

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: ORM (Object-Relational Mapping)
- **Alembic**: Database migration tool
- **Jinja2**: Template engine (built into Flask)
- **SQLite**: Database (default, configurable)

## Configuration

Edit `config.py` to customize:

- Database URL: `SQLALCHEMY_DATABASE_URI`
- Secret key: `SECRET_KEY`
- Session timeout: `PERMANENT_SESSION_LIFETIME`

## Error Handling

The application includes:
- 404 error page for missing routes
- 500 error page for server errors
- Form validation with user feedback
- Database transaction rollback on errors

## Notes

- The application uses SQLite by default (`horse_races.db`)
- To use a different database (PostgreSQL, MySQL, etc.), update `SQLALCHEMY_DATABASE_URI` in `config.py`
- All horse and jockey names must be unique
- Race participants are unique per race (same horse-jockey pair cannot be added twice)

## License

This is a demonstration project. Use freely for educational purposes.
