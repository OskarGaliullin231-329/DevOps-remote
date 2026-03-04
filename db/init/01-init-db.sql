create database horse_races;

create user horse_races_admin with password 'hr_pass';

grant all privileges on database horse_races to horse_races_admin;
grant all privileges on all tables in schema public to horse_races_admin;
grant all privileges on all sequences in schema public to horse_races_admin;
