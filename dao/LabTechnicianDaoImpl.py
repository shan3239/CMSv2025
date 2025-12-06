from typing import List, Dict, Optional
from pymysql.cursors import DictCursor

from dao.AbstractLabTechnicianDao import LabTechnicianDaoService
from DbConnection.ConnectionDB import ConnectionDB


class LabTechnicianDaoImpl(LabTechnicianDaoService):
    """
    DAO implementation for Lab Technician use cases.
    """

    def __init__(self):
        self.conn = ConnectionDB().get_connection()

    # ---------- Lab Test Management ----------

    def list_lab_tests(self) -> List[Dict]:
        sql = """
        SELECT lab_test_id, test_name, category, description,
               normal_range, units, status
        FROM LAB_TEST
        ORDER BY test_name
        """
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print("Error listing lab tests:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    def add_lab_test(self, test_data: Dict) -> Optional[int]:
        sql = """
        INSERT INTO LAB_TEST
        (test_name, category, description, normal_range, units, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                sql,
                (
                    test_data.get("test_name"),
                    test_data.get("category"),
                    test_data.get("description"),
                    test_data.get("normal_range"),
                    test_data.get("units"),
                    test_data.get("status", "Active"),
                ),
            )
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error adding lab test:", e)
            return None
        finally:
            if cursor:
                cursor.close()

    def update_lab_test(self, lab_test_id: int, field_name: str, value) -> bool:
        allowed_fields = ["test_name", "category", "description", "normal_range", "units", "status"]
        if field_name not in allowed_fields:
            print("Invalid field for update in LAB_TEST.")
            return False

        sql = f"UPDATE LAB_TEST SET {field_name} = %s WHERE lab_test_id = %s"
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (value, lab_test_id))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error updating lab test:", e)
            return False
        finally:
            if cursor:
                cursor.close()

    # ---------- Lab Orders & Results ----------

    def list_pending_lab_orders(self) -> List[Dict]:
        sql = """
        SELECT lo.lab_order_id,
               lo.ordered_at,
               lo.status,
               lo.notes,
               p.patient_id,
               p.full_name AS patient_name,
               s.full_name AS doctor_name
        FROM LAB_ORDER lo
        JOIN PATIENT p ON lo.patient_id = p.patient_id
        JOIN DOCTOR d ON lo.doctor_id = d.doctor_id
        JOIN STAFF s ON d.staff_id = s.staff_id
        WHERE lo.status IN ('Pending', 'In Progress')
        ORDER BY lo.ordered_at DESC
        """
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print("Error listing pending lab orders:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    def get_lab_order_header(self, lab_order_id: int) -> Optional[Dict]:
        sql = """
        SELECT lo.lab_order_id,
               lo.ordered_at,
               lo.status,
               lo.notes,
               p.patient_id,
               p.full_name AS patient_name,
               d.doctor_id,
               s.full_name AS doctor_name
        FROM LAB_ORDER lo
        JOIN PATIENT p ON lo.patient_id = p.patient_id
        JOIN DOCTOR d ON lo.doctor_id = d.doctor_id
        JOIN STAFF s ON d.staff_id = s.staff_id
        WHERE lo.lab_order_id = %s
        """
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql, (lab_order_id,))
            return cursor.fetchone()
        except Exception as e:
            print("Error fetching lab order header:", e)
            return None
        finally:
            if cursor:
                cursor.close()

    def get_lab_order_items_with_results(self, lab_order_id: int) -> List[Dict]:
        sql = """
        SELECT loi.lab_order_item_id,
               lt.lab_test_id,
               lt.test_name,
               lt.category,
               loi.notes AS item_notes,
               lr.result_id,
               lr.result_value,
               lr.units AS result_units,
               lr.result_date,
               lr.comments
        FROM LAB_ORDER_ITEM loi
        JOIN LAB_TEST lt ON loi.lab_test_id = lt.lab_test_id
        LEFT JOIN LAB_RESULT lr ON loi.lab_order_item_id = lr.lab_order_item_id
        WHERE loi.lab_order_id = %s
        ORDER BY lt.test_name
        """
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql, (lab_order_id,))
            return cursor.fetchall()
        except Exception as e:
            print("Error fetching lab order items:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    def insert_or_update_lab_result(
        self,
        lab_order_item_id: int,
        result_value: str,
        units: str,
        comments: str,
        technician_staff_id: int,
    ) -> bool:
        """
        If result exists for this item -> UPDATE
        Else -> INSERT
        """
        select_sql = "SELECT result_id FROM LAB_RESULT WHERE lab_order_item_id = %s"
        insert_sql = """
        INSERT INTO LAB_RESULT
        (lab_order_item_id, result_value, units, result_date, comments, technician_staff_id)
        VALUES (%s, %s, %s, NOW(), %s, %s)
        """
        update_sql = """
        UPDATE LAB_RESULT
        SET result_value = %s,
            units = %s,
            result_date = NOW(),
            comments = %s,
            technician_staff_id = %s
        WHERE lab_order_item_id = %s
        """

        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(select_sql, (lab_order_item_id,))
            row = cursor.fetchone()

            if row:
                # Update
                cursor.execute(
                    update_sql,
                    (result_value, units, comments, technician_staff_id, lab_order_item_id),
                )
            else:
                # Insert
                cursor.execute(
                    insert_sql,
                    (lab_order_item_id, result_value, units, comments, technician_staff_id),
                )

            self.conn.commit()
            return True
        except Exception as e:
            print("Error inserting/updating lab result:", e)
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def update_lab_order_status(self, lab_order_id: int, status: str) -> bool:
        sql = """
        UPDATE LAB_ORDER
        SET status = %s
        WHERE lab_order_id = %s
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (status, lab_order_id))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error updating lab order status:", e)
            return False
        finally:
            if cursor:
                cursor.close()

    def are_all_results_entered(self, lab_order_id: int) -> bool:
        """
        Checks if every LAB_ORDER_ITEM has a LAB_RESULT.
        """
        sql = """
        SELECT
            (SELECT COUNT(*) FROM LAB_ORDER_ITEM WHERE lab_order_id = %s) AS total_items,
            (SELECT COUNT(DISTINCT lab_order_item_id) FROM LAB_RESULT
             WHERE lab_order_item_id IN (
                 SELECT lab_order_item_id FROM LAB_ORDER_ITEM WHERE lab_order_id = %s
             )) AS items_with_results
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (lab_order_id, lab_order_id))
            row = cursor.fetchone()
            if not row:
                return False
            total_items = row[0]
            items_with_results = row[1]
            return total_items > 0 and total_items == items_with_results
        except Exception as e:
            print("Error checking results completion:", e)
            return False
        finally:
            if cursor:
                cursor.close()
