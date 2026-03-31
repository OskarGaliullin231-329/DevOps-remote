# Docker Deployment Guide

## Overview
This project is fully containerized using Docker and Docker Compose with three main services:
- **PostgreSQL 17 Alpine** - Database with automatic initialization
- **Python 3.14 slim-trixie** - Flask application with Gunicorn
- **Nginx Alpine** - Web server (reverse proxy on port 5000)

## Prerequisites
- Docker 20.10+
- Docker Compose 1.29+

## Quick Start

### Build and Start Services
```bash
# Build all images and start containers
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f app
docker-compose logs -f postgres
docker-compose logs -f nginx
```

### Stop Services
```bash
# Stop all containers
docker-compose down

# Stop and remove volumes (WARNING: deletes database data)
docker-compose down -v
```

## Services Details

### PostgreSQL (`postgres` service)
- **Image**: postgres:17-alpine
- **Port**: 5432 (exposed for debugging)
- **Database**: `horse_races`
- **User**: `horse_races_admin`
- **Password**: `hr_pass`
- **Initialization**: Automatically runs `/db/init_db.sql` on first start
- **Data**: Persisted in Docker volume `postgres_data`

### Application (`app` service)
- **Image**: python:3.14-slim-trixie
- **Port**: 5000 (internal, exposed via nginx)
- **Features**:
  - Waits for PostgreSQL to be ready
  - Automatically populates database with sample data via `init_data.py`
  - Runs Gunicorn with 4 workers
  - Hot-reload for `templates/` and `static/` directories
- **Logs**: Check with `docker-compose logs app`

### Nginx (`nginx` service)
- **Image**: nginx:alpine
- **Port**: 5000 (exposed to host)
- **Function**: Reverse proxy to Flask application
- **Config**: `nginx.conf`
- **Features**:
  - Gzip compression
  - Static file caching
  - Proper header forwarding

## Accessing the Application
Once running, access the application at:
```
http://localhost:5000
```

## Common Commands

### Database Debugging
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U horse_races_admin -d horse_races

# View database contents
docker-compose exec postgres psql -U horse_races_admin -d horse_races -c "\dt"
```

### Application Debugging
```bash
# View application logs
docker-compose logs -f app

# Execute command in running app container
docker-compose exec app python -c "from app import app; app.app_context().push(); print('OK')"

# Interactive shell in app container
docker-compose exec app /bin/bash
```

### Rebuild Services
```bash
# Rebuild specific service
docker-compose build postgres
docker-compose build app

# Rebuild and restart
docker-compose up --build postgres
```

## Environment Variables

### PostgreSQL Configuration
- `POSTGRES_DB` - Database name (default: `horse_races`)
- `POSTGRES_USER` - Database user (default: `horse_races_admin`)
- `POSTGRES_PASSWORD` - Database password (default: `hr_pass`)

### Flask Application Configuration
- `DB_USER` - Database user (default: `horse_races_admin`)
- `DB_PASS` - Database password (default: `hr_pass`)
- `DB_HOST` - Database host (default: `postgres`)
- `DB_PORT` - Database port (default: `5432`)
- `DB_NAME` - Database name (default: `horse_races`)
- `FLASK_ENV` - Flask environment (default: `production`)
- `SECRET_KEY` - Flask secret key (default: `dev-secret-key-change-in-production`)

To override, create a `.env` file:
```
DB_PASS=your_secure_password
SECRET_KEY=your_secret_key
```

Then update `docker-compose.yml` to use env_file.

## Troubleshooting

### Application crashes with "PostgreSQL is unavailable"
- Wait for PostgreSQL to fully start (check `docker-compose logs postgres`)
- Use `docker-compose down -v` to remove old volume and start fresh

### Port 5000 already in use
```bash
# Find process using port 5000
lsof -i :5000

# Or change port in docker-compose.yml: `"8080:5000"`
```

### Database not initialized
- Check PostgreSQL logs: `docker-compose logs postgres`
- Verify `db/init_db.sql` exists and is readable
- Delete volume and restart: `docker-compose down -v && docker-compose up -d`

### Sample data not loaded
- Check app logs: `docker-compose logs app`
- Verify `init_data.py` script syntax
- Check database connectivity from app container

## Production Considerations

1. **Security**:
   - Change default database password in `docker-compose.yml`
   - Use strong Flask `SECRET_KEY`
   - Don't expose PostgreSQL port in production
   - Use environment variables from secure source

2. **Performance**:
   - Adjust Gunicorn workers (in `Dockerfile.app`)
   - Use Nginx upstream load balancing if scaling
   - Enable Redis for session management

3. **Monitoring**:
   - Add health checks (already included)
   - Set up log aggregation
   - Monitor container resource usage

4. **Updates**:
   - Regularly update base images
   - Pin specific versions in production
   - Test updates in staging first

## File Structure
```
app/
├── Dockerfile.postgres    # PostgreSQL container definition
├── Dockerfile.app         # Flask application container definition
├── nginx.conf             # Nginx reverse proxy configuration
├── docker-compose.yml     # Docker Compose orchestration
├── .dockerignore          # Files to exclude from docker builds
├── app.py                 # Flask application
├── config.py              # Configuration
├── models.py              # SQLAlchemy models
├── init_data.py           # Sample data initialization
├── requirements.txt       # Python dependencies
├── db/
│   ├── init_db.sql        # Database schema initialization
│   └── drop_db.sql        # Database cleanup script
├── templates/             # HTML templates
└── static/                # Static files (CSS, JS, images)
```
