
from database.db_connection import create_connection
from utils.validators import validate_customer_data
from mysql.connector import Error


def get_all_customers():

    connection = create_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT *
            FROM customers
            WHERE is_deleted = 0
            ORDER BY customer_id
        """

        cursor.execute(query)

        customers = cursor.fetchall()

        return customers

    except Error as e:
        print("Error fetching customers:", e)
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_customer(name, email, phone, gender, city, registration_date):

    # Validate customer information
    errors = validate_customer_data(
        name, email, phone, gender, city, registration_date
    )

    if errors:
        print("\nCustomer Validation Failed:")

        for error in errors:
            print("-", error)

        return False

    # Clean and standardize input
    name = name.strip()
    email = email.strip().lower()
    phone = str(phone).strip()
    gender = gender.strip().capitalize()
    city = city.strip()

    connection = create_connection()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO customers
            (customer_name, email, phone, gender, city,
             registration_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            name, email, phone, gender, city, registration_date
        )

        cursor.execute(query, values)
        connection.commit()

        print("Customer added successfully!")
        return True

    except Error as e:
        connection.rollback()

        if e.errno == 1062:
            print("A customer with this email already exists.")
        else:
            print("Error adding customer:", e)

        return False

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()



def update_customer(customer_id, name, email, phone, gender, city, registration_date):

    # Validate customer information
    errors = validate_customer_data(
        name, email, phone, gender, city, registration_date
    )

    if errors:
        print("\nCustomer Validation Failed:")

        for error in errors:
            print("-", error)

        return False

    # Clean and standardize input
    name = name.strip()
    email = email.strip().lower()
    phone = str(phone).strip()
    gender = gender.strip().capitalize()
    city = city.strip()

    connection = create_connection()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            UPDATE customers
            SET customer_name = %s,
                email = %s,
                phone = %s,
                gender = %s,
                city = %s,
                registration_date = %s
            WHERE customer_id = %s
            AND is_deleted = 0
        """

        values = (
            name, email, phone, gender, city,
            registration_date, customer_id
        )

        cursor.execute(query, values)
        connection.commit()

        if cursor.rowcount > 0:
            print("Customer updated successfully!")
            return True
        else:
            print("Customer not found or no changes made.")
            return False

    except Error as e:
        connection.rollback()

        if e.errno == 1062:
            print("Another customer already uses this email.")
        else:
            print("Error updating customer:", e)

        return False

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


def archive_customer(customer_id):

    connection = create_connection()

    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        query = """
            UPDATE customers
            SET is_deleted = 1,
                archived_at = NOW()
            WHERE customer_id = %s
            AND is_deleted = 0
        """

        cursor.execute(query, (customer_id,))
        connection.commit()

        if cursor.rowcount > 0:
            print("Customer archived successfully!")
            return True
        else:
            print("Customer not found or already archived.")
            return False

    except Error as e:
        print("Error archiving customer:", e)
        return False

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
def restore_customer(customer_id):

    connection = create_connection()

    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        query = """
            UPDATE customers
            SET is_deleted = 0,
                archived_at = NULL
            WHERE customer_id = %s
            AND is_deleted = 1
        """

        cursor.execute(query, (customer_id,))
        connection.commit()

        if cursor.rowcount > 0:
            print("Customer restored successfully!")
            return True
        else:
            print("Customer not found or is not archived.")
            return False

    except Error as e:
        print("Error restoring customer:", e)
        return False

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def search_customer(search_value):

    connection = create_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT *
            FROM customers
            WHERE is_deleted = 0
            AND (
                customer_name LIKE %s
                OR email LIKE %s
                OR city LIKE %s
            )
            ORDER BY customer_id
        """

        search_pattern = f"%{search_value}%"

        cursor.execute(
            query,
            (search_pattern, search_pattern, search_pattern)
        )

        customers = cursor.fetchall()

        return customers

    except Error as e:
        print("Error searching customers:", e)
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
def get_archived_customers():

    connection = create_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT *
            FROM customers
            WHERE is_deleted = 1
            ORDER BY archived_at DESC
        """

        cursor.execute(query)

        customers = cursor.fetchall()

        return customers

    except Error as e:
        print("Error fetching archived customers:", e)
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_customer_by_id(customer_id):

    connection = create_connection()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT *
            FROM customers
            WHERE customer_id = %s
            AND is_deleted = 0
        """

        cursor.execute(query, (customer_id,))

        customer = cursor.fetchone()

        return customer

    except Error as e:
        print("Error fetching customer:", e)
        return None

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()
def get_customer_count():

    connection = create_connection()

    if connection is None:
        return 0

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            SELECT COUNT(*)
            FROM customers
            WHERE is_deleted = 0
        """

        cursor.execute(query)

        result = cursor.fetchone()

        return result[0]

    except Error as e:
        print("Error counting customers:", e)
        return 0

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()

def bulk_import_customers(customer_records):

    connection = create_connection()

    report = {
        "imported": 0,
        "failed": 0,
        "errors": []
    }

    if connection is None:
        report["errors"].append("Database connection failed.")
        report["failed"] = len(customer_records)
        return report

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO customers
            (
                customer_name,
                email,
                phone,
                gender,
                city,
                registration_date
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        for index, customer in enumerate(customer_records, start=2):

            name = customer.get("customer_name")
            email = customer.get("email")
            phone = customer.get("phone")
            gender = customer.get("gender")
            city = customer.get("city")
            registration_date = customer.get("registration_date")

            # Handle phone numbers read as numeric Excel values
            if phone is not None:
                phone = str(phone).strip()

                if phone.endswith(".0"):
                    phone = phone[:-2]

            # Convert date objects into MySQL-compatible strings
            if hasattr(registration_date, "strftime"):
                registration_date = registration_date.strftime("%Y-%m-%d")

            errors = validate_customer_data(
                name,
                email,
                phone,
                gender,
                city,
                registration_date
            )

            if errors:
                report["failed"] += 1
                report["errors"].append(
                    f"Row {index}: {'; '.join(errors)}"
                )
                continue

            try:
                cursor.execute(
                    query,
                    (
                        name.strip(),
                        email.strip(),
                        phone,
                        gender.strip(),
                        city.strip(),
                        registration_date
                    )
                )

                connection.commit()
                report["imported"] += 1

            except Error as e:

                connection.rollback()
                report["failed"] += 1

                if e.errno == 1062:
                    message = "Duplicate email address."
                else:
                    message = str(e)

                report["errors"].append(
                    f"Row {index}: {message}"
                )

    except Error as e:
        connection.rollback()
        report["errors"].append(f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()

    return report


if __name__ == "__main__":

    customer_id = 15

    print("\n--- RESTORE TEST ---")

    restore_customer(customer_id)

    print("\n--- ACTIVE CUSTOMERS ---")
    customers = get_all_customers()
    print("Total Active Customers:", len(customers))

    print("\n--- ARCHIVED CUSTOMERS ---")
    archived = get_archived_customers()
    print("Total Archived Customers:", len(archived))


