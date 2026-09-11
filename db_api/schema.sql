Use honeypot;
create table if not exists logins(

    id int auto_increment primary key,
    ip varchar(40),
    user_agent text,
    username varchar(255),
    password varchar(255),
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    country TEXT,
    is_automated boolean
);

create table if not exists ssh(

    id int auto_increment primary key,
    ip varchar(40),
    username varchar(255),
    password varchar(255),
    client_version varchar(255),
    cipher varchar(255),
    mac varchar(255),
    compression varchar(255),
    connection_timestamp DATETIME(6),
    COLUMN session_duration_seconds FLOAT
);