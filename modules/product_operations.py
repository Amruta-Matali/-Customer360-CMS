
from mysql.connector import Error
from database.db_connection import create_connection


def get_all_products():

    connection = create_connection()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                product_id,
                product_name,
                category,
                price,
                stock_quantity,
                created_at
            FROM products
            ORDER BY product_id
        """

        cursor.execute(query)

        products = cursor.fetchall()

        return products

    except Error as e:
        print("Error fetching products:", e)
        return []

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


def add_product(product_name, category, price, stock_quantity):

    connection = create_connection()

    if connection is None:
        return False

    cursor = None

    try:
        # Input validation
        product_name = str(product_name).strip()
        category = str(category).strip()

        if not product_name:
            print("Product name cannot be empty.")
            return False

        try:
            price = float(price)
            stock_quantity = int(stock_quantity)
        except (ValueError, TypeError):
            print("Price and stock quantity must be valid numbers.")
            return False

        import math

        if not math.isfinite(price) or price < 0:
            print("Price must be a valid non-negative number.")
            return False

        if stock_quantity < 0:
            print("Stock quantity cannot be negative.")
            return False

        cursor = connection.cursor()

        query = """
            INSERT INTO products
            (product_name, category, price, stock_quantity)
            VALUES (%s, %s, %s, %s)
        """

        values = (
            product_name,
            category,
            price,
            stock_quantity
        )

        cursor.execute(query, values)

        connection.commit()

        print("Product added successfully!")
        return True

    except Error as e:
        connection.rollback()
        print("Error adding product:", e)
        return False

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()

def update_product(product_id, product_name, category, price, stock_quantity):

    connection = create_connection()

    if connection is None:
        return False

    cursor = None

    try:
        product_name = str(product_name).strip()
        category = str(category).strip()

        if not product_name:
            print("Product name cannot be empty.")
            return False

        try:
            price = float(price)
            stock_quantity = int(stock_quantity)
        except (ValueError, TypeError):
            print("Price and stock quantity must be valid numbers.")
            return False

        import math

        if not math.isfinite(price) or price < 0:
            print("Price must be a valid non-negative number.")
            return False

        if stock_quantity < 0:
            print("Stock quantity cannot be negative.")
            return False

        cursor = connection.cursor()

        query = """
            UPDATE products
            SET
                product_name = %s,
                category = %s,
                price = %s,
                stock_quantity = %s
            WHERE product_id = %s
        """

        values = (
            product_name,
            category,
            price,
            stock_quantity,
            product_id
        )

        cursor.execute(query, values)

        if cursor.rowcount == 0:
            print("Product not found or no changes made.")
            return False

        connection.commit()

        print("Product updated successfully!")
        return True

    except Error as e:
        connection.rollback()
        print("Error updating product:", e)
        return False

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()

