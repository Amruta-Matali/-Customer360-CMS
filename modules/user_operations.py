
import bcrypt

from database.db_connection import create_connection


def create_user(username, email, password):

    if not username or not email or not password:
        print("Username, email and password are required.")
        return False

    if len(password) < 8:
        print("Password must contain at least 8 characters.")
        return False

    connection = create_connection()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        # Hash the password before storing it
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        query = """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (username.strip(), email.strip().lower(), password_hash)
        )

        connection.commit()

        print("User created successfully!")
        return True

    except Exception as e:
        connection.rollback()
        print("User Creation Error:", e)
        return False

    finally:
        if cursor:
            cursor.close()
        connection.close()


def authenticate_user(login, password):

    connection = create_connection()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT user_id, username, email, password_hash, status
            FROM users
            WHERE username = %s OR email = %s
            LIMIT 1
        """

        login = login.strip()

        cursor.execute(
            query,
            (login, login.lower())
        )

        user = cursor.fetchone()

        if not user:
            return None

        if user["status"] != "Active":
            return None

        password_matches = bcrypt.checkpw(
            password.encode("utf-8"),
            user["password_hash"].encode("utf-8")
        )

        if password_matches:

            return {
                "user_id": user["user_id"],
                "username": user["username"],
                "email": user["email"]
            }

        return None

    except Exception as e:
        print("Authentication Error:", e)
        return None

    finally:
        if cursor:
            cursor.close()
        connection.close()
