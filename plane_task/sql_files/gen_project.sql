USE Terminal

DROP TABLE IF EXISTS tickets
DROP TABLE IF EXISTS flight_order
DROP TABLE IF EXISTS ticket_types
DROP TABLE IF EXISTS staff
DROP TABLE IF EXISTS passengers
DROP TABLE IF EXISTS flight_trip
DROP TABLE IF EXISTS aircraft
DROP TABLE IF EXISTS login_credentials


CREATE TABLE aircraft
(
    aircraft_id INT IDENTITY(1,1) PRIMARY KEY,
    flight BIT,
    flight_capacity INT,
    aircraft_type VARCHAR(10)
)


CREATE TABLE flight_trip
(
    flight_trip_id INT IDENTITY(1,1) PRIMARY KEY,
    ticket_price FLOAT,
    aircraft_id int,
    destination VARCHAR(30),
    duration FLOAT,
    origin VARCHAR(30),
    FOREIGN KEY (aircraft_id) REFERENCES aircraft(aircraft_id)
    ON DELETE SET NULL
)


CREATE TABLE passengers
(
    passengers_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name VARCHAR(20),
    second_name VARCHAR(20),
    age FLOAT,
    passport_number VARCHAR(20) ,
)

CREATE TABLE ticket_types
(
    ticket_type VARCHAR(10) PRIMARY KEY,
    discount FLOAT
)

CREATE TABLE flight_order
(
    ticket_number INT IDENTITY(1,1) PRIMARY KEY,
    ticket_type VARCHAR(10),
    ticket_value float,
    flight_trip_id INT,
    FOREIGN KEY (ticket_type) REFERENCES ticket_types(ticket_type)
    ON DELETE CASCADE,
    FOREIGN KEY (flight_trip_id) REFERENCES flight_trip(flight_trip_id)
    ON DELETE CASCADE
)

CREATE TABLE tickets
(
    passengers_id INT,
    ticket_number INT,
    FOREIGN KEY (passengers_id) REFERENCES passengers(passengers_id)
    ON DELETE CASCADE,
    FOREIGN KEY (ticket_number) REFERENCES flight_order(ticket_number)
    ON DELETE CASCADE
)


CREATE TABLE staff
(
    staff_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name VARCHAR(30),
    second_name VARCHAR(30),
    age INT,
    flight_trip_id INT,
    FOREIGN KEY (flight_trip_id) REFERENCES flight_trip(flight_trip_id)
    ON DELETE SET NULL
)

CREATE TABLE login_credentials (
    username VARCHAR(40) NOT NULL,
    salt VARCHAR(50) NOT NULL,
    password VARCHAR(200) NOT NULL
)


INSERT INTO ticket_types
VALUES ('adult', 1), ('child', 0.5), ('infant', 0.25)

INSERT INTO aircraft
VALUES (0,20, 'plane')
