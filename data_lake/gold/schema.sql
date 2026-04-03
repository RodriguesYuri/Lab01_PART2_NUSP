CREATE TABLE dim_location (
    locationid INT PRIMARY KEY,
    borough TEXT,
    zone TEXT,
    service_zone TEXT
);

CREATE TABLE fact_trips (
    id SERIAL PRIMARY KEY,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    passenger_count INT,
    trip_distance FLOAT,
    fare_amount FLOAT,
    total_amount FLOAT,
    pulocationid INT,
    dolocationid INT,
    payment_type INT
);