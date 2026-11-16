
from database.db_connection import create_connection

tables = [
    "customers",
    "products",
    "orders",
    "order_details",
    "feedback",
    "users"
]

connection = create_connection()

if connection is None:
    print("Database connection failed.")
else:
    try:
        cursor = connection.cursor()

        with open("database_structure.sql", "w", encoding="utf-8") as file:
            file.write("CREATE DATABASE IF NOT EXISTS customer_management;\n")
            file.write("USE customer_management;\n\n")

            for table in tables:
                cursor.execute(f"SHOW CREATE TABLE `{table}`")
                result = cursor.fetchone()

                file.write(result[1] + ";\n\n")

        print("Database structure exported successfully!")
        print("File created: database_structure.sql")

    except Exception as error:
        print("Export Error:", error)

    finally:
        cursor.close()
        connection.close()
