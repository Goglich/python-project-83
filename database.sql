CREATE TABLE urls (
    id INT primary key generated always as identity NOT NULL,
    name varchar(255),
    created_at date DEFAULT CURRENT_DATE
);


CREATE TABLE url_checks (
    id INT primary key generated always as identity NOT NULL, 
    url_id INT NOT NULL, 
    status_code INT, 
    h1 varchar(255), 
    title varchar(255), 
    description text,
    created_at date DEFAULT CURRENT_DATE
);