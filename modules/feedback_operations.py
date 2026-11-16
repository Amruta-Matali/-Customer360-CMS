from mysql.connector import Error
from database.db_connection import create_connection


def add_feedback(customer_id, rating, comments, feedback_date):

    connection = create_connection()

    if connection is None:
        return False

    cursor = None

    try:
        if not 1 <= int(rating) <= 5:
            print("Rating must be between 1 and 5.")
            return False

        cursor = connection.cursor()

        # Verify that the customer exists and is active
        cursor.execute(
            """
            SELECT customer_id
            FROM customers
            WHERE customer_id = %s AND is_deleted = 0
            """,
            (customer_id,)
        )

        if cursor.fetchone() is None:
            print("Customer not found or archived.")
            return False

        cursor.execute(
            """
            INSERT INTO feedback
            (customer_id, rating, comments, feedback_date)
            VALUES (%s, %s, %s, %s)
            """,
            (customer_id, rating, comments, feedback_date)
        )

        feedback_id = cursor.lastrowid

        connection.commit()

        print("Feedback added successfully!")
        print("Feedback ID:", feedback_id)

        return feedback_id

    except (Error, ValueError, TypeError) as e:
        connection.rollback()
        print("Feedback insertion failed:", e)
        return False

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()
def get_all_feedback():

    connection = create_connection()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                f.feedback_id,
                f.customer_id,
                c.customer_name,
                f.rating,
                f.comments,
                f.feedback_date
            FROM feedback f
            JOIN customers c
                ON f.customer_id = c.customer_id
            ORDER BY f.feedback_id DESC
        """

        cursor.execute(query)

        feedback_records = cursor.fetchall()

        return feedback_records

    except Error as e:
        print("Error fetching feedback:", e)
        return []

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()
def bulk_import_feedback(feedback_records):

    connection = create_connection()

    if connection is None:
        return {
            "imported": 0,
            "failed": len(feedback_records),
            "errors": ["Database connection failed."]
        }

    cursor = None

    imported = 0
    failed = 0
    errors = []

    try:
        cursor = connection.cursor(dictionary=True)

        for index, record in enumerate(feedback_records, start=1):

            try:
                email = str(record["customer_email"]).strip()
                rating = int(record["rating"])
                comments = str(record.get("comments", "") or "").strip()

                feedback_date = record["feedback_date"]

                if isinstance(feedback_date, datetime):
                    feedback_date = feedback_date.date()

                elif isinstance(feedback_date, str):
                    feedback_date = datetime.strptime(
                        feedback_date, "%Y-%m-%d"
                    ).date()

                if not email:
                    raise ValueError("Customer email is required.")

                if rating < 1 or rating > 5:
                    raise ValueError("Rating must be between 1 and 5.")

                if not isinstance(feedback_date, date):
                    raise ValueError("Invalid feedback date.")

                cursor.execute(
                    """
                    SELECT customer_id
                    FROM customers
                    WHERE email = %s AND is_deleted = 0
                    """,
                    (email,)
                )

                customer = cursor.fetchone()

                if customer is None:
                    raise ValueError(
                        f"No active customer found for email: {email}"
                    )

                cursor.execute(
                    """
                    INSERT INTO feedback
                    (customer_id, rating, comments, feedback_date)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        customer["customer_id"],
                        rating,
                        comments,
                        feedback_date
                    )
                )

                connection.commit()
                imported += 1

            except (Error, ValueError, KeyError, TypeError) as e:

                connection.rollback()
                failed += 1
                errors.append(f"Row {index}: {e}")

        return {
            "imported": imported,
            "failed": failed,
            "errors": errors
        }

    except Error as e:

        connection.rollback()
        print("Bulk feedback import failed:", e)

        return {
            "imported": imported,
            "failed": failed,
            "errors": errors + [str(e)]
        }

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()
