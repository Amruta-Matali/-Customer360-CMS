
from mysql.connector import Error
from database.db_connection import create_connection
from decimal import Decimal, InvalidOperation


def create_order(customer_id, order_date, order_items,
                 payment_status="Pending",
                 order_status="Processing"):

    connection = create_connection()

    if connection is None:
        return False

    cursor = None

    try:
        if not order_items:
            print("An order must contain at least one product.")
            return False

        cursor = connection.cursor()

        # 1. Verify that the customer exists and is not archived
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

        # 2. Calculate order total using database product prices
        order_total = Decimal("0.00")
        order_lines = []

        for item in order_items:

            product_id = int(item["product_id"])
            quantity = int(item["quantity"])

            if quantity <= 0:
                raise ValueError("Product quantity must be greater than zero.")

            cursor.execute(
                """
                SELECT price
                FROM products
                WHERE product_id = %s
                """,
                (product_id,)
            )

            product = cursor.fetchone()

            if product is None:
                raise ValueError(
                    f"Product ID {product_id} does not exist."
                )

            price = Decimal(str(product[0]))

            line_total = price * quantity
            order_total += line_total

            order_lines.append(
                (product_id, quantity, price)
            )

        # 3. Insert the main order
        cursor.execute(
            """
            INSERT INTO orders
            (
                customer_id,
                order_date,
                total_amount,
                payment_status,
                order_status
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                customer_id,
                order_date,
                order_total,
                payment_status,
                order_status
            )
        )

        order_id = cursor.lastrowid

        # 4. Insert all purchased products
        detail_query = """
            INSERT INTO order_details
            (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """

        for product_id, quantity, price in order_lines:

            cursor.execute(
                detail_query,
                (order_id, product_id, quantity, price)
            )

        # 5. Save everything together
        connection.commit()

        print("Order created successfully!")
        print("Order ID:", order_id)
        print("Order Total:", order_total)

        return order_id

    except (Error, ValueError, KeyError, TypeError, InvalidOperation) as e:

        connection.rollback()
        print("Order creation failed:", e)
        return False

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()
def get_all_orders():

    connection = create_connection()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                o.order_id,
                c.customer_name,
                o.order_date,
                o.total_amount,
                o.payment_status,
                o.order_status
            FROM orders o
            JOIN customers c
                ON o.customer_id = c.customer_id
            ORDER BY o.order_id DESC
        """

        cursor.execute(query)

        orders = cursor.fetchall()

        return orders

    except Error as e:
        print("Error fetching orders:", e)
        return []

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()
def update_order_status(order_id, payment_status, order_status):

    valid_payment_statuses = [
        "Pending", "Paid", "Failed", "Refunded"
    ]

    valid_order_statuses = [
        "Processing", "Shipped", "Delivered", "Cancelled"
    ]

    if payment_status not in valid_payment_statuses:
        print("Invalid payment status.")
        return False

    if order_status not in valid_order_statuses:
        print("Invalid order status.")
        return False

    connection = create_connection()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        # Check whether the order exists
        cursor.execute(
            "SELECT order_id FROM orders WHERE order_id = %s",
            (order_id,)
        )

        if cursor.fetchone() is None:
            print("Order not found.")
            return False

        # Update payment and order status
        cursor.execute(
            """
            UPDATE orders
            SET payment_status = %s,
                order_status = %s
            WHERE order_id = %s
            """,
            (payment_status, order_status, order_id)
        )

        connection.commit()

        print("Order status updated successfully!")
        return True

    except Error as e:
        connection.rollback()
        print("Order update failed:", e)
        return False

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()
def get_order_details(order_id):

    connection = create_connection()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                od.order_detail_id,
                od.order_id,
                p.product_name,
                od.quantity,
                od.price,
                (od.quantity * od.price) AS subtotal
            FROM order_details od
            JOIN products p
                ON od.product_id = p.product_id
            WHERE od.order_id = %s
            ORDER BY od.order_detail_id
        """

        cursor.execute(query, (order_id,))

        order_details = cursor.fetchall()

        return order_details

    except Error as e:
        print("Error fetching order details:", e)
        return []

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()
def get_customer_orders(customer_id):

    connection = create_connection()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                order_id,
                customer_id,
                order_date,
                total_amount,
                payment_status,
                order_status
            FROM orders
            WHERE customer_id = %s
            ORDER BY order_date DESC, order_id DESC
        """

        cursor.execute(query, (customer_id,))

        orders = cursor.fetchall()

        return orders

    except Error as e:
        print("Error fetching customer orders:", e)
        return []

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()
