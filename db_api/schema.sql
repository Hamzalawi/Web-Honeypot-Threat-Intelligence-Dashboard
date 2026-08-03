create table logins(

    id int auto_increment primary key,
    ip varchar(40),
    user_agent text,
    username varchar(255),
    password varchar(255),
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    country TEXT,
    is_bot boolean
);