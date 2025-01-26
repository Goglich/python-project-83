CREATE TABLE urls (
    id INT primary key generated always as identity NOT NULL,
    name varchar(255),
    created_at timestamp
);