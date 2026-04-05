# Migration Setup Summary

✅ Flask-Migrate is now fully configured for local development and CLI usage!

## What Was Done

### 1. **Fixed Migration Configuration**
   - Updated `app/alembic.ini` with correct paths
   - Fixed `app/migrations/env.py` for proper Flask integration
   - Ensured models are auto-discovered for migrations

### 2. **Created Initial Migration**
   - `app/migrations/versions/001_initial.py` - Creates all database tables from models

### 3. **Documentation**
   - `MIGRATIONS.md` - Complete guide to using migrations
   - `MIGRATION_EXAMPLES.md` - Real-world examples and recipes
   - `app/MIGRATIONS_CHEATSHEET.sh` - Quick command reference

---

## Quick Start

### First-time setup:
```bash
# Go to project root
cd /home/oscar/Documents/DevOps/application

# Install dependencies (if not done)
pip install -r requirements.txt

# Create database
psql -U postgres -f db/init_db.sql

# Configure environment and apply migrations from project root
cd /home/oscar/Documents/DevOps/application
export FLASK_APP=app.app
export PYTHONPATH=.

# Apply migrations
flask db upgrade

# (Optional) Load sample data
python -m app.init_data
```

### Run these commands from project root:

```bash
cd /home/oscar/Documents/DevOps/application
export FLASK_APP=app.app
export PYTHONPATH=.
flask db current

# View all applied migrations  
flask db history

# Create new migration (auto-detect model changes)
flask db migrate -m "Your description here"

# Apply pending migrations
flask db upgrade

# Revert last migration
flask db downgrade
```

---

## File Structure

```
app/
├── alembic.ini                 ← Database connection config
├── models.py                   ← Your model definitions
├── migrations/
│   ├── env.py                  ← Flask-Alembic integration
│   ├── script.py.mako          ← Migration template
│   ├── versions/
│   │   └── 001_initial.py      ← Initial migration
│   └── __init__.py
└── config.py                   ← Connection string builder
```

---

## How It Works

1. **Models** (`app/models.py`) - Define your database schema
2. **Create Migration** - Run `flask db migrate` to auto-generate SQL
3. **Review** - Check the generated file in `app/migrations/versions/`
4. **Apply** - Run `flask db upgrade` to execute SQL changes
5. **Version Control** - Commit migration files to git

---

## Examples

### Add a new field to Horse model:
```bash
# 1. Edit models.py
nano app/models.py
# Add: color = db.Column(db.String(50))

# 2. Generate migration
cd app
flask db migrate -m "Add color field to horses"

# 3. Apply it
flask db upgrade
```

### Revert recent changes:
```bash
cd app
flask db downgrade  # Rollback once
flask db downgrade  # Rollback twice
flask db upgrade    # Rollback forward
```

---

## Key Files to Know

| File | Purpose |
|------|---------|
| `MIGRATIONS.md` | ← Read this for detailed guide |
| `MIGRATION_EXAMPLES.md` | ← Real-world scenarios |
| `app/MIGRATIONS_CHEATSHEET.sh` | ← Command reference |
| `app/alembic.ini` | Configuration file |
| `app/migrations/env.py` | Flask integration layer |
| `app/migrations/versions/` | Your migration scripts |

---

## Troubleshooting

**Command not working?**
- Make sure you're in `app/` directory
- Run: `echo $PWD` → should end with `/app`

**"Can't find models"?**
- Ensure models.py exists in app/
- Check alembic.ini path is correct

**Database won't connect?**
- Verify PostgreSQL is running
- Check DB credentials in config.py or env vars

**See the docs!**
- Detailed: `MIGRATIONS.md`
- Examples: `MIGRATION_EXAMPLES.md`
- Commands: `app/MIGRATIONS_CHEATSHEET.sh`

---

## Environment Variables (Optional)

Override database connection:
```bash
export DB_USER=your_user
export DB_PASS=your_pass
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=horse_races

# Or use full URL:
export DATABASE_URL="postgresql://user:pass@localhost/dbname"
```

---

**Ready to go!** 🚀

Start with migrations by reading `MIGRATIONS.md` or running:
```bash
cd app && flask db history
```
