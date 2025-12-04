from DbConnection.ConnectionDb import ConnectionDb
from models.Staff import Staff

class AdminDao:

    # Create staff (Admin UC: Manage Staff)
    def create_staff(self, staff: Staff):
        conn = ConnectionDb.get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO STAFF (full_name, email, phone, username, password_hash, role_id, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (staff.full_name, staff.email, staff.phone, staff.username,
                  staff.password_hash, staff.role_id, staff.status)

        cursor.execute(sql, values)
        conn.commit()

        return cursor.rowcount, cursor.lastrowid

    # Update staff details
    def update_staff(self, staff_id, full_name=None, email=None, phone=None, role_id=None, status=None):
        conn = ConnectionDb.get_connection()
        cursor = conn.cursor()

        sql = """
        UPDATE STAFF
        SET full_name = %s, email = %s, phone = %s, role_id = %s, status = %s
        WHERE staff_id = %s
        """

        cursor.execute(sql, (full_name, email, phone, role_id, status, staff_id))
        conn.commit()

        return cursor.rowcount

    # Deactivate Staff
    def deactivate_staff(self, staff_id):
        conn = ConnectionDb.get_connection()
        cursor = conn.cursor()

        sql = "UPDATE STAFF SET status = 'Inactive' WHERE staff_id = %s"
        cursor.execute(sql, (staff_id,))
        conn.commit()

        return cursor.rowcount

    # List all staff
    def list_staff(self):
        conn = ConnectionDb.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM STAFF")
        return cursor.fetchall()

    # View system logs (Admin UC: Audit Logs)
    def view_audit_logs(self):
        conn = ConnectionDb.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM AUDIT_LOG ORDER BY action_timestamp DESC")
        return cursor.fetchall()

    # Manage Roles (Admin UC)
    def list_roles(self):
        conn = ConnectionDb.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ROLE")
        return cursor.fetchall()
