
from database.db_connection import create_connection


def get_dashboard_statistics():

    connection = create_connection()

    if connection is None:
        return {}

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                COUNT(*) AS total_customers,
                SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END)
                    AS active_customers,
                SUM(CASE WHEN status = 'Inactive' THEN 1 ELSE 0 END)
                    AS inactive_customers
            FROM customers
            WHERE is_deleted = 0
        """

        cursor.execute(query)

        result = cursor.fetchone()

        return result

    except Exception as e:
        print("Dashboard Error:", e)
        return {}

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


def get_customers_by_city():

    connection = create_connection()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                COALESCE(NULLIF(city, ''), 'Unknown') AS city,
                COUNT(*) AS customer_count
            FROM customers
            WHERE is_deleted = 0
            GROUP BY city
            ORDER BY customer_count DESC
        """

        cursor.execute(query)

        result = cursor.fetchall()

        return result

    except Exception as e:
        print("City Chart Error:", e)
        return []

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()
def get_registration_trend():

    connection = create_connection()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                DATE_FORMAT(registration_date, '%Y-%m') AS registration_month,
                COUNT(*) AS customer_count
            FROM customers
            WHERE is_deleted = 0
            GROUP BY DATE_FORMAT(registration_date, '%Y-%m')
            ORDER BY registration_month
        """

        cursor.execute(query)

        result = cursor.fetchall()

        return result

    except Exception as e:
        print("Registration Trend Error:", e)
        return []

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


