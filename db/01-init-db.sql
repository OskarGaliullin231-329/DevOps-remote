create database horse_races;

create user horse_races_admin with password 'hr_pass';

grant all privileges on database horse_races to horse_races_admin;
grant all privileges on all tables in schema public to horse_races_admin;
grant all privileges on all sequences in schema public to horse_races_admin;

\connect horse_races

create table hosts (
    id        serial primary key,
    host_name varchar(255),
    surname   varchar(255)
);

create table jockeys (
    id          serial primary key,
    jockey_name varchar(255) not null,
    rating      integer
);

create table races (
    id        serial primary key,
    race_date date not null
);

create table horses (
    id         serial primary key,
    host_id    integer not null references hosts(id),
    horse_name varchar(255) not null,
    rating     integer
);

create table races_results (
    id        serial primary key,
    horse_id  integer not null references horses(id),
    jockey_id integer not null references jockeys(id),
    race_id   integer not null references races(id),
    place     integer
);
