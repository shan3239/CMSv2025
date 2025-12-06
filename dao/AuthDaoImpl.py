from pymysql.cursors import DictCursor
from DbConnection.ConnectionDB import ConnectionDB
from models.staff import Staff


class AuthDaoImpl:
    """
    DAO for authentication operations.
    """

    LOGIN_QUERY = """
        SELECT s.staff_id, s.full_name, s.email, s.phone, s.username, 
               s.password_hash, s.role_id, s.status,
               r.role_name
        FROM STAFF s
        JOIN ROLE r ON s.role_id = r.role_id
        WHERE s.username = %s AND s.password_hash = %s AND s.status = 'Active'
    """

    def __init__(self):
        self.conn = ConnectionDB().get_connection()

    def authenticate_user(self, username: str, password: str):
        """Check login credentials and return Staff object."""
        cursor = None

        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.LOGIN_QUERY, (username, password))
            row = cursor.fetchone()

            if row:
                return Staff(
                    staff_id=row["staff_id"],
                    full_name=row["full_name"],
                    email=row["email"],
                    phone=row["phone"],
                    username=row["username"],
                    password_hash=row["password_hash"],
                    role_id=row["role_id"],
                    status=row["status"],
                    role_name=row["role_name"]
                )
            return None

        except Exception as e:
            print("Error during authentication:", e)
            return None

        finally:
            if cursor:
                cursor.close()
