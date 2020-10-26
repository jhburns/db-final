import load_schema

print("Welcome to the airline manager 2000")
connection = load_schema.initialize_db()

if connection is None:
    print("Error! initializing the db failed. Exiting.")
else:
    print("Connected to the database file: airline.db")
    print()

    connection.close()
