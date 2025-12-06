import re

def validate_staff_name(name: str):
    if not name or len(name.strip()) == 0:
        raise Exception("Staff name cannot be empty.")

    name = name.strip()

    if len(name) < 3:
        raise Exception("Staff name must be at least 3 characters long.")

    # Only letters and spaces allowed
    pattern = r"^[A-Za-z\s]+$"
    if not re.match(pattern, name):
        raise Exception("Staff name should contain only alphabets and spaces.")

    return True


def validate_email(email: str):
    if not email or email.strip() == "":
        raise Exception("Email ID is required.")

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.match(pattern, email):
        raise Exception("Invalid email format.")

    return True


def validate_username(username: str):
    if not username or len(username.strip()) == 0:
        raise Exception("Username cannot be empty.")
    pattern = r"^[A-Za-z0-9_]{3,30}$"
    if not re.match(pattern, username):
        raise Exception("Invalid username. Use 3–30 letters, numbers or underscore.")
    return True


def validate_role_id(role_id: str):
    if not role_id:
        raise Exception("Role ID is required.")
    try:
        rid = int(role_id)
        if rid <= 0:
            raise Exception("Role ID must be positive.")
    except ValueError:
        raise Exception("Role ID must be a valid integer.")
    return True
