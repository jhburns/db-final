PRAGMA strict=ON;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS customers (
	customer_id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	weight_kg INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS planes (
	serial_number TEXT PRIMARY KEY,
	seat_count_row INTEGER NOT NULL,
	seat_count_column INTEGER NOT NULL,
	max_load_kg INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS inventory (
	inventory_id INTEGER PRIMARY KEY,
	plane_id INTEGER NOT NULL,
	FOREIGN KEY(plane_id) REFERENCES planes(serial_number) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS flights (
	flight_id INTEGER PRIMARY KEY,
	departure_datetime TEXT NOT NULL,
	i_id INTEGER NOT NULL,
	FOREIGN KEY(i_id) REFERENCES inventory(inventory_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS passengers (
	passenger_id INTEGER NOT NULL,
	f_id INTEGER NOT NULL,
	FOREIGN KEY(passenger_id) REFERENCES customers(customer_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY(f_id) REFERENCES flights(flight_id) ON DELETE CASCADE ON UPDATE CASCADE
);