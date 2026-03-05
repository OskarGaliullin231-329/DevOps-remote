\connect horse_races

create table if not exists hosts (
    id        serial primary key,
    host_name varchar(255),
    surname   varchar(255)
);

create table if not exists jockeys (
    id          serial primary key,
    jockey_name varchar(255) not null,
    rating      integer
);

create table if not exists races (
    id        serial primary key,
    race_date date not null
);

create table if not exists horses (
    id         serial primary key,
    host_id    integer not null references hosts(id),
    horse_name varchar(255) not null,
    rating     integer
);

create table if not exists races_results (
    id        serial primary key,
    horse_id  integer not null references horses(id),
    jockey_id integer not null references jockeys(id),
    race_id   integer not null references races(id),
    place     integer
);
