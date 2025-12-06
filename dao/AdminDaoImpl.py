from typing import List, Dict, Optional
from pymysql.cursors import DictCursor

from dao.AbstractAdminDao import AdminDaoService
from DbConnection.ConnectionDB import ConnectionDB
from models.staff import Staff


class AdminDaoImpl(AdminDaoService):
    """
    DAO implementation for Admin operations:
    Staff management, roles, logs, departments
    """

    # ====================== SQL QUERIES ======================

    INSERT_STAFF = """
        INSERT INTO STAFF (full_name, email, phone, username, password_hash, role_id, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    SELECT_ALL_STAFF = """
        SELECT s.staff_id, s.full_name, s.email, s.phone, s.username, s.password_hash,
               s.role_id, s.status, r.role_name
        FROM STAFF s
        JOIN ROLE r ON s.role_id = r.role_id
        ORDER BY s.staff_id
    """

    SELECT_STAFF_BY_ID = """
        SELECT s.staff_id, s.full_name, s.email, s.phone, s.username, s.password_hash,
               s.role_id, s.status, r.role_name
        FROM STAFF s
        JOIN ROLE r ON s.role_id = r.role_id
        WHERE s.staff_id = %s
    """

    DEACTIVATE_STAFF = """
        UPDATE STAFF SET status = 'Inactive' WHERE staff_id = %s
    """

    DELETE_STAFF = """
        DELETE FROM STAFF WHERE staff_id = %s
    """

    # dynamic field update (field name validated in Lib layer)
    UPDATE_FIELD = "UPDATE STAFF SET {} = %s WHERE staff_id = %s"

    SELECT_ROLES = """
        SELECT role_id, role_name FROM ROLE ORDER BY role_id
    """

    SELECT_DEPARTMENTS = """
        SELECT department_id, department_name, description, status FROM DEPARTMENT
        ORDER BY department_id
    """

    SELECT_AUDIT_LOGS = """
        SELECT log_id, staff_id, action_type, entity_name, entity_id, description, action_timestamp
        FROM AUDIT_LOG
        ORDER BY action_timestamp DESC
        LIMIT 25
    """

    # ====================== INIT ======================

    def __init__(self):
        self.conn = ConnectionDB().get_connection()

    # ====================== STAFF CRUD ======================

    def create_staff(self, staff: Staff) -> bool:
        """Insert new staff record"""
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                self.INSERT_STAFF,
                (
                    staff.full_name,
                    staff.email,
                    staff.phone,
                    staff.username,
                    staff.password_hash,
                    staff.role_id,
                    staff.status,
                ),
            )
            self.conn.commit()
            return cursor.rowcount == 1

        except Exception as e:
            print("Error inserting staff:", e)
            return False

        finally:
            if cursor:
                cursor.close()

    def list_staff(self) -> List[Staff]:
        """Return list of all staff"""
        staff_list = []
        cursor = None

        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.SELECT_ALL_STAFF)
            rows = cursor.fetchall()

            for row in rows:
                staff_obj = Staff(
                    staff_id=row["staff_id"],
                    full_name=row["full_name"],
                    email=row["email"],
                    phone=row["phone"],
                    username=row["username"],
                    password_hash=row["password_hash"],
                    role_id=row["role_id"],
                    status=row["status"],
                    role_name=row["role_name"],
                )
                staff_list.append(staff_obj)

        except Exception as e:
            print("Error listing staff:", e)

        finally:
            if cursor:
                cursor.close()

        return staff_list

    def get_staff_by_id(self, staff_id: int) -> Optional[Staff]:
        """Return a single Staff object by ID"""
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.SELECT_STAFF_BY_ID, (staff_id,))
            row = cursor.fetchone()

            if not row:
                return None

            return Staff(
                staff_id=row["staff_id"],
                full_name=row["full_name"],
                email=row["email"],
                phone=row["phone"],
                username=row["username"],
                password_hash=row["password_hash"],
                role_id=row["role_id"],
                status=row["status"],
                role_name=row["role_name"],
            )

        except Exception as e:
            print("Error fetching staff by ID:", e)
            return None

        finally:
            if cursor:
                cursor.close()

    def deactivate_staff(self, staff_id: int) -> bool:
        """Set staff status = Inactive"""
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.DEACTIVATE_STAFF, (staff_id,))
            self.conn.commit()
            return cursor.rowcount == 1

        except Exception as e:
            print("Error deactivating staff:", e)
            return False

        finally:
            if cursor:
                cursor.close()

    def delete_staff(self, staff_id: int) -> bool:
        """Hard delete staff"""
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.DELETE_STAFF, (staff_id,))
            self.conn.commit()
            return cursor.rowcount == 1

        except Exception as e:
            print("Error deleting staff:", e)
            return False

        finally:
            if cursor:
                cursor.close()

    def update_staff_field(self, staff_id: int, field_name: str, value) -> bool:
        """Update a single field of STAFF"""
        cursor = None
        try:
            sql = self.UPDATE_FIELD.format(field_name)
            cursor = self.conn.cursor()
            cursor.execute(sql, (value, staff_id))
            self.conn.commit()
            return cursor.rowcount == 1

        except Exception as e:
            print("Error updating staff field:", e)
            return False

        finally:
            if cursor:
                cursor.close()

    # ====================== ROLES ======================

    def list_roles(self) -> List[Dict]:
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.SELECT_ROLES)
            return cursor.fetchall()

        except Exception as e:
            print("Error listing roles:", e)
            return []

        finally:
            if cursor:
                cursor.close()

    # ====================== DEPARTMENTS ======================

    def list_departments(self) -> List[Dict]:
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.SELECT_DEPARTMENTS)
            return cursor.fetchall()

        except Exception as e:
            print("Error listing departments:", e)
            return []

        finally:
            if cursor:
                cursor.close()

    # ====================== AUDIT LOGS ======================

    def list_audit_logs(self) -> List[Dict]:
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.SELECT_AUDIT_LOGS)
            return cursor.fetchall()

        except Exception as e:
            print("Error listing audit logs:", e)
            return []

        finally:
            if cursor:
                cursor.close()
