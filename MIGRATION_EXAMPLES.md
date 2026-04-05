# Flask-Migrate Examples & Recipes

## Getting Started

### 1. First-Time Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create database and user
psql -U postgres -f db/init_db.sql

# Set package environment and run from project root
cd /home/oscar/Documents/DevOps/application
export FLASK_APP=app.app
export PYTHONPATH=.

# Apply initial migration
flask db upgrade

# Verify it worked
flask db current
```

### 2. Initialize Sample Data (Optional)
```bash
cd /home/oscar/Documents/DevOps/application
export FLASK_APP=app.app
export PYTHONPATH=.
python -m app.init_data
```

---

## Common Scenarios

### Scenario A: Add a New Column to Existing Table

**Step 1: Update the model**
```python
# app/models.py
class Horse(db.Model):
    __tablename__ = 'horses'
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'), nullable=False)
    horse_name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer)
    # NEW COLUMN:
    age = db.Column(db.Integer)
```

**Step 2: Create migration**
```bash
cd app
flask db migrate -m "Add age column to horses"
```

**Step 3: Review generated migration**
```bash
# Check: app/migrations/versions/XXX_add_age_column_to_horses.py
nano app/migrations/versions/*add_age*.py
```

**Step 4: Apply migration**
```bash
flask db upgrade
```

**Step 5: Verify**
```bash
flask db current
# Now you can use horse.age in your code
```

---

### Scenario B: Rename a Column

**Step 1: Update model**
```python
# Change jockey_name to name (or whatever the new name is)
class Jockey(db.Model):
    __tablename__ = 'jockeys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # Was jockey_name
    rating = db.Column(db.Integer)
```

**Step 2: Create migration** (this will be a basic one, needs manual editing)
```bash
cd app
flask db migrate -m "Rename jockey_name to name"
```

**Step 3: Edit the migration to use rename_column**
```python
# app/migrations/versions/XXX_rename_jockey_name_to_name.py
def upgrade() -> None:
    op.alter_column('jockeys', 'jockey_name',
               new_column_name='name')

def downgrade() -> None:
    op.alter_column('jockeys', 'name',
               new_column_name='jockey_name')
```

**Step 4: Apply**
```bash
flask db upgrade
```

---

### Scenario C: Add a Foreign Key Constraint

**Step 1: Update model**
```python
# app/models.py
class RaceResult(db.Model):
    __tablename__ = 'races_results'
    # ... existing columns ...
    # NEW: Add relationship if not already there
    race = db.relationship('Race', backref='results')
```

**Step 2: Generate migration**
```bash
cd app
flask db migrate -m "Add foreign key constraint to races_results"
```

**Step 3: Apply**
```bash
flask db upgrade
```

---

### Scenario D: Add a Unique Constraint

**Method 1: Auto-generate (recommended)**
```bash
cd app
flask db migrate -m "Add unique constraint on host names"
flask db upgrade
```

**Method 2: Manual migration**
```python
# In migration file:
def upgrade() -> None:
    op.create_unique_constraint('uq_host_name', 'hosts', ['host_name'])

def downgrade() -> None:
    op.drop_constraint('uq_host_name', 'hosts')
```

---

### Scenario E: Revert Latest Change

If you want to undo the last migration:

```bash
cd app

# See what was applied
flask db history

# Downgrade one step
flask db downgrade

# Verify current state
flask db current
```

---

### Scenario F: Start Fresh (Reset Migrations)

⚠️ **WARNING: This deletes all migration history!** Only use for development:

```bash
cd app

# Delete all migration files
rm -rf migrations/versions/*

# Delete the old migration tracking (if using PostgreSQL)
python -c "
import psycopg2
from app import app
conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS alembic_version')
conn.commit()
conn.close()
"

# Create fresh initial migration
flask db migrate -m "Initial migration (fresh start)"
flask db upgrade

# Re-initialize sample data
python init_data.py
```

---

## Troubleshooting

### Error: "No module named 'models'"
```bash
# Make sure you're in app directory
cd /path/to/app
flask db ...
```

### Error: "Can't locate Revision 'abc123'"
```bash
# Your version tracking is out of sync. Reset it:
# 1. Delete old migrations: rm -rf migrations/versions/*
# 2. Create new: flask db migrate -m "Initial"
# 3. Apply: flask db upgrade
```

### Error: "Connection to database failed"
```bash
# Verify PostgreSQL is running and accessible:
psql -U horse_races_admin -h localhost -d horse_races

# Check config in app/config.py or environment variables:
echo $DB_HOST
echo $DB_USER
echo $DB_NAME
```

### Migration not detecting my model changes
```bash
# Make sure:
# 1. Model has __tablename__
# 2. Model inherits from db.Model
# 3. Model file is imported in app.py or migrations/env.py
# Then try: flask db migrate --autogenerate -m "..."
```

---

## Tips & Best Practices

1. **Always review migrations before applying:**
   ```bash
   cat app/migrations/versions/*latest*.py
   ```

2. **Test reversibility in development:**
   ```bash
   flask db upgrade  # Apply
   flask db downgrade  # Revert
   flask db upgrade  # Apply again
   ```

3. **Use descriptive messages:**
   ```bash
   # Good:
   flask db migrate -m "Add unique constraint on email column"
   
   # Bad:
   flask db migrate -m "Fix"
   ```

4. **Keep migrations in version control:**
   ```bash
   git add app/migrations/versions/
   git commit -m "Add migration: ..."
   ```

5. **For production, always test migrations first:**
   ```bash
   # On staging database:
   flask db upgrade
   # Verify everything works
   # Then do on production
   ```

---

## File Locations

```
app/
├── alembic.ini                 # Alembic configuration
├── config.py                   # Database connection config
├── models.py                   # SQLAlchemy model definitions
├── migrations/
│   ├── env.py                  # Alembic environment
│   ├── script.py.mako          # Migration template
│   └── versions/
│       ├── 001_initial.py      # Initial migration
│       ├── 002_add_field.py    # Your first new migration
│       └── ...
└── MIGRATIONS_CHEATSHEET.sh    # Quick command reference
```

---

## Advanced: Custom Migration

For complex migrations, you can manually create one:

```bash
cd app
flask db revision -m "My custom migration"
```

Then edit `app/migrations/versions/XXX_my_custom_migration.py`:

```python
def upgrade() -> None:
    # Your custom SQL using op.execute()
    op.execute("UPDATE horses SET rating = 10 WHERE rating IS NULL")
    
def downgrade() -> None:
    op.execute("UPDATE horses SET rating = NULL WHERE rating = 10")
```

Apply with:
```bash
flask db upgrade
```
