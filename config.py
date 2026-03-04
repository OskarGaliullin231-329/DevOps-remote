import os
from datetime import timedelta

class Config:
    """Configuration for Flask app

    The database URI is constructed from several environment variables so
    that the application can be pointed at the PostgreSQL database created
    by `db/init_db.sql`.  The SQL script creates a database called
    ``horse_races`` and a user ``horse_races_admin`` without a password.
    You can override any part of the connection string by setting the
    ``DATABASE_URL`` environment variable directly (this is what
    ``SQLALCHEMY_DATABASE_URI`` will end up containing).
    """
    # credentials used by the SQL initialization script
    DB_USER = os.getenv('DB_USER', 'horse_races_admin')
    DB_PASS = os.getenv('DB_PASS', 'hr_pass')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'horse_races')

    # construct a sensible default URI but allow DATABASE_URL override
    if DB_PASS:
        default_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        default_url = f"postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', default_url)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
