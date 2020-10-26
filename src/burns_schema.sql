CREATE TABLE customers (
	customer_id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	weight_kg INTEGER NOT NULL
);

CREATE TABLE planes (
	serial_number TEXT PRIMARY KEY,
	seat_count_row INTEGER NOT NULL,
	seat_count_column INTEGER NOT NULL,
	max_weight_kg INTEGER NOT NULL
);

CREATE TABLE inventory (
	inventory_id INTEGER PRIMARY KEY,
	plane_id INTEGER NOT NULL,
	FOREIGN KEY(plane_id) REFERENCES planes(serial_number)
);

CREATE TABLE flights (
	flight_id INTEGER NOT NULL PRIMARY KEY,
	date TEXT NOT NULL,
	i_id INTEGER NOT NULL,
	FOREIGN KEY(i_id) REFERENCES planes(inventory_id)
);

CREATE TABLE passengers (
	passenger_id INTEGER NOT NULL,
	f_id INTEGER NOT NULL,
	FOREIGN KEY(passenger_id) REFERENCES customers(customer_id),
	FOREIGN KEY(f_id) REFERENCES flights(flight_id)
);