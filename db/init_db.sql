-- initialization script for PostgreSQL
-- creates a dedicated database and user for the application
-- you may wish to set a password for the user if your pg_hba.conf
-- requires it (e.g. `ALTER USER horse_races_admin WITH PASSWORD 'secret';`)

create database horse_races;

create user horse_races_admin with password 'hr_pass';

grant all privileges on database horse_races to horse_races_admin;
grant all privileges on all tables in schema public to horse_races_admin;
grant all privileges on all sequences in schema public to horse_races_admin;

\c horse_races
