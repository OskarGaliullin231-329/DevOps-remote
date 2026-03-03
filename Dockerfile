FROM python:3.14-bookworm

WORKDIR /app

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system deps (including build tools for psycopg2)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

ENV FLASK_APP=app.py

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app", "--workers", "3", "--worker-class", "gthread"]
