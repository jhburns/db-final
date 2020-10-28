import load_schema
import models
import actions

print("Welcome to the airline manager 2000")
connection = load_schema.initialize_db()

if connection is None:
    print("Error! initializing the db failed. Exiting.")
else:
    print("Connected to the database file: airline.db")
    print()

    table = models.tables["customers"]
    key = table[0]
    sql = actions.generate_delete("customers", key)

    actions.execute(connection, sql, [1])

    connection.close()
