# Database Migrations Guide

This project uses **Flask-Migrate** (Alembic) for database migrations. Migrations allow you to version control your database schema changes.

## Setup

### Prerequisites
- PostgreSQL running locally (or update `DATABASE_URL` in config)
- Python dependencies installed: `pip install -r requirements.txt`
- Flask app in `app/` directory

### Initial Configuration

1. **Create the database and user:**
```bash
psql -U postgres -f db/init_db.sql
```

2. **Apply initial migration:**
```bash
cd /home/oscar/Documents/DevOps/application
export FLASK_APP=app.app
export PYTHONPATH=.
flask db upgrade
```

## Common Commands

All commands should be run from the project root with package imports configured:

```bash
cd /home/oscar/Documents/DevOps/application
export FLASK_APP=app.app
export PYTHONPATH=.
```

### View current database version
```bash
flask db current
```

### View all applied migrations
```bash
flask db history
```

### Apply pending migrations
```bash
flask db upgrade
```

### Rollback one migration
```bash
flask db downgrade
```

### Create automatic migration (detects model changes)
```bash
flask db migrate -m "Add new column to users"
```

### Create empty migration (manual editing required)
```bash
flask db revision -m "Create new index"
```

## Workflow

### When you modify models:

1. **Update model definition** in `app/models.py`

2. **Generate migration script:**
```bash
flask db migrate -m "Descriptive message"
```

3. **Review the generated migration** in `app/migrations/versions/`

4. **Apply the migration:**
```bash
flask db upgrade
```

### Example: Adding a new field

```python
# models.py - Add new field to existing model
class Horse(db.Model):
    __tablename__ = 'horses'
    id = db.Column(db.Integer, primary_key=True)
    horse_name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer)
    breed = db.Column(db.String(100))  # NEW FIELD
```

```bash
# Generate migration
cd app
flask db migrate -m "Add breed field to horses"

# Apply it
flask db upgrade
```

## Configuration

### Database connection
Edit `app/config.py` or set environment variables:

```bash
export DB_USER=horse_races_admin
export DB_PASS=hr_pass
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=horse_races
```

Or override completely:
```bash
export DATABASE_URL="postgresql://user:password@host:5432/dbname"
```

### Migration files location
- Scripts: `app/migrations/versions/`
- Configuration: `app/alembic.ini`
- Environment: `app/migrations/env.py`

## Troubleshooting

### "Can't locate Revision identified by 'non-existent'" error
This means your migrations folder is out of sync. Solution:

```bash
# Reset all migrations (WARNING: deletes all migration history)
rm -rf app/migrations/versions/*

# Create new initial migration from current models
cd app
flask db migrate -m "Initial migration"
flask db upgrade
```

### "ModuleNotFoundError: No module named 'models'"
Make sure you're running commands from the `app/` directory:

```bash
cd app
flask db upgrade
```

### Connection refused
Check PostgreSQL is running and connection details:

```bash
# Test connection
psql -U horse_races_admin -h localhost -d horse_races
```

## Best Practices

1. **Always review generated migrations** before applying
2. **Test migrations with `downgrade` then `upgrade`** to ensure reversibility
3. **Use descriptive messages:** `flask db migrate -m "Add email unique constraint to hosts"`
4. **Keep migrations small** - one logical change per migration
5. **Never manually edit applied migration files** - create new ones instead
6. **Commit migration files to git** along with model changes

## Integration with Docker

When running in containers, migrations are automatically applied on startup via the entrypoint script. To manually run migrations in a running container:

```bash
docker compose exec app flask db upgrade
```
