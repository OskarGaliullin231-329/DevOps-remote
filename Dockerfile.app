FROM python:3.14-slim-trixie

WORKDIR /app

# Устанавливаем зависимости системы для PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение
COPY . .

# Создаем entrypoint скрипт для инициализации и запуска приложения
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "Waiting for PostgreSQL to be ready..."\n\
until PGPASSWORD=${DB_PASS} psql -h ${DB_HOST} -U ${DB_USER} -d ${DB_NAME} -c "SELECT 1" 2>/dev/null; do\n\
  echo "PostgreSQL is unavailable, waiting..."\n\
  sleep 1\n\
done\n\
echo "PostgreSQL is ready!"\n\
\n\
echo "Initializing sample data..."\n\
python init_data.py\n\
\n\
echo "Starting Gunicorn server..."\n\
exec gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 60 app:app\n\
' > /entrypoint.sh && chmod +x /entrypoint.sh

# Переменные окружения по умолчанию
ENV DB_USER=horse_races_admin
ENV DB_PASS=hr_pass
ENV DB_HOST=postgres
ENV DB_PORT=5432
ENV DB_NAME=horse_races
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
