from typing import Optional
from dao.AuthDaoImpl import AuthDaoImpl
from models.staff import Staff


class AuthLib:
    """
    Authentication Library
    """

    auth_service = AuthDaoImpl()

    @staticmethod
    def login(username: str, password: str) -> Optional[Staff]:
        """
        Perform login using DAO.
        Returns Staff object if valid, else None.
        """
        if not username.strip() or not password.strip():
            print("Username and password required.")
            return None

        staff_obj = AuthLib.auth_service.authenticate_user(username, password)

        if staff_obj:
            print(f"\nLogin success! Welcome, {staff_obj.full_name} ({staff_obj.role_name}).")
            return staff_obj
        else:
            print("Invalid username or password.\n")
            return None
