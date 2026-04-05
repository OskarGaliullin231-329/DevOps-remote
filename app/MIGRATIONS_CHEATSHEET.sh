#!/bin/bash
# Flask-Migrate Quick Reference
# Run these commands from the app/ directory

cd app

# ============================================================================
# SETUP & DIAGNOSTICS
# ============================================================================

# Initialize migrations folder (only first time, already done)
# flask db init

# Show current database version
flask db current

# Show migration history
flask db history

# Generate SQL for migration without applying
flask db upgrade --sql

# ============================================================================
# CREATING MIGRATIONS
# ============================================================================

# Auto-detect model changes and create migration
flask db migrate -m "Add new field to horses table"

# Create empty migration for manual editing
flask db revision -m "Custom index on race_date"

# ============================================================================
# APPLYING MIGRATIONS
# ============================================================================

# Apply all pending migrations
flask db upgrade

# Upgrade to specific revision
flask db upgrade f2d3b4a

# Rollback one migration
flask db downgrade

# Rollback to specific revision
flask db downgrade f2d3b4a

# ============================================================================
# WORKFLOW EXAMPLE
# ============================================================================

# 1. Edit models.py - add new field
# 2. Generate migration
#    flask db migrate -m "Add breed column to horses"
#
# 3. Review the file: app/migrations/versions/XXX_add_breed_column_to_horses.py
#
# 4. Apply it
#    flask db upgrade
#
# 5. Verify
#    flask db current

# ============================================================================
# USEFUL HELPERS
# ============================================================================

# Test migration without applying (useful for CI/CD)
python -c "from alembic import command; command.upgrade(config, 'head')"

# Show what migrations would do in SQL
flask db upgrade --sql | head -30

# List all available branches
flask db branches
