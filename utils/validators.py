
import re
from datetime import datetime, date


def validate_customer_data(
    name, email, phone, gender, city, registration_date
):

    errors = []

    # 1. Validate customer name
    if not name or not name.strip():
        errors.append("Customer name cannot be empty.")
    elif len(name.strip()) > 100:
        errors.append("Customer name cannot exceed 100 characters.")

    # 2. Validate email
    email = email.strip() if email else ""

    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not email:
        errors.append("Email cannot be empty.")
    elif not re.match(email_pattern, email):
        errors.append("Please enter a valid email address.")

    # 3. Validate phone number
    phone = str(phone).strip() if phone is not None else ""

    if not re.fullmatch(r"\d{10}", phone):
        errors.append("Phone number must contain exactly 10 digits.")

    # 4. Validate gender
    valid_genders = ["Male", "Female", "Other"]

    if not gender or gender.strip().capitalize() not in valid_genders:
        errors.append("Gender must be Male, Female or Other.")

    # 5. Validate city
    if not city or not city.strip():
        errors.append("City cannot be empty.")
    elif len(city.strip()) > 50:
        errors.append("City cannot exceed 50 characters.")

    # 6. Validate registration date
    try:
        if isinstance(registration_date, datetime):
            parsed_date = registration_date.date()
        elif isinstance(registration_date, date):
            parsed_date = registration_date
        else:
            parsed_date = datetime.strptime(
                str(registration_date), "%Y-%m-%d"
            ).date()

        if parsed_date > date.today():
            errors.append("Registration date cannot be in the future.")

    except (ValueError, TypeError):
        errors.append("Registration date must be in YYYY-MM-DD format.")

    return errors
