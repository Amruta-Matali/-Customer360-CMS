from database.db_connection import create_connection

connection = create_connection()

if connection:

    print("Connection Test Passed!")

    connection.close()

    print("Database Connection Closed.")

else:

    print("Connection Test Failed!")
