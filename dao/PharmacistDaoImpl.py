from typing import List, Dict, Optional
from pymysql.cursors import DictCursor

from dao.AbstractPharmacistDao import PharmacistDaoService
from DbConnection.ConnectionDB import ConnectionDB


class PharmacistDaoImpl(PharmacistDaoService):
    """
    DAO implementation for Pharmacist use cases.
    """

    def __init__(self):
        self.conn = ConnectionDB().get_connection()

    # ---------- Medicine & Inventory ----------

    def list_medicines_with_stock(self) -> List[Dict]:
        sql = """
        SELECT m.medicine_id,
               m.medicine_name,
               m.category,
               m.form,
               m.strength,
               m.status,
               COALESCE(SUM(b.quantity_on_hand), 0) AS total_stock
        FROM MEDICINE m
        LEFT JOIN MEDICINE_BATCH b ON m.medicine_id = b.medicine_id
        GROUP BY m.medicine_id, m.medicine_name, m.category, m.form, m.strength, m.status
        ORDER BY m.medicine_name
        """
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print("Error listing medicines:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    def add_medicine(self, med_data: Dict) -> Optional[int]:
        sql = """
        INSERT INTO MEDICINE
        (medicine_name, category, form, strength, status)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                sql,
                (
                    med_data.get("medicine_name"),
                    med_data.get("category"),
                    med_data.get("form"),
                    med_data.get("strength"),
                    med_data.get("status", "Active"),
                ),
            )
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error adding medicine:", e)
            return None
        finally:
            if cursor:
                cursor.close()

    def add_medicine_batch(self, batch_data: Dict) -> Optional[int]:
        sql = """
        INSERT INTO MEDICINE_BATCH
        (medicine_id, batch_number, expiry_date,
         quantity_on_hand, reorder_level, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                sql,
                (
                    batch_data.get("medicine_id"),
                    batch_data.get("batch_number"),
                    batch_data.get("expiry_date"),
                    batch_data.get("quantity_on_hand"),
                    batch_data.get("reorder_level"),
                    batch_data.get("status", "Active"),
                ),
            )
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error adding medicine batch:", e)
            return None
        finally:
            if cursor:
                cursor.close()

    def list_batches_for_medicine(self, medicine_id: int) -> List[Dict]:
        sql = """
        SELECT batch_id, batch_number, expiry_date,
               quantity_on_hand, reorder_level, status
        FROM MEDICINE_BATCH
        WHERE medicine_id = %s
        ORDER BY expiry_date
        """
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql, (medicine_id,))
            return cursor.fetchall()
        except Exception as e:
            print("Error listing batches:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    def update_batch_quantity(self, batch_id: int, new_qty: int) -> bool:
        sql = """
        UPDATE MEDICINE_BATCH
        SET quantity_on_hand = %s
        WHERE batch_id = %s
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (new_qty, batch_id))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error updating batch quantity:", e)
            return False
        finally:
            if cursor:
                cursor.close()

    def get_low_stock_batches(self) -> List[Dict]:
        sql = """
        SELECT b.batch_id,
               b.medicine_id,
               m.medicine_name,
               b.batch_number,
               b.quantity_on_hand,
               b.reorder_level,
               b.expiry_date,
               b.status
        FROM MEDICINE_BATCH b
        JOIN MEDICINE m ON b.medicine_id = m.medicine_id
        WHERE b.status = 'Active'
          AND b.reorder_level IS NOT NULL
          AND b.quantity_on_hand <= b.reorder_level
        ORDER BY b.quantity_on_hand ASC
        """
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print("Error getting low stock batches:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    # ---------- Expiry Management ----------

    def list_near_expiry_batches(self, days: int) -> List[Dict]:
        sql = """
        SELECT b.batch_id,
               b.medicine_id,
               m.medicine_name,
               b.batch_number,
               b.expiry_date,
               b.quantity_on_hand,
               b.status
        FROM MEDICINE_BATCH b
        JOIN MEDICINE m ON b.medicine_id = m.medicine_id
        WHERE b.status = 'Active'
          AND b.expiry_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL %s DAY)
        ORDER BY b.expiry_date
        """
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql, (days,))
            return cursor.fetchall()
        except Exception as e:
            print("Error getting near-expiry batches:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    def list_expired_batches(self) -> List[Dict]:
        sql = """
        SELECT b.batch_id,
               b.medicine_id,
               m.medicine_name,
               b.batch_number,
               b.expiry_date,
               b.quantity_on_hand,
               b.status
        FROM MEDICINE_BATCH b
        JOIN MEDICINE m ON b.medicine_id = m.medicine_id
        WHERE b.status = 'Active'
          AND b.expiry_date < CURDATE()
        ORDER BY b.expiry_date
        """
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print("Error getting expired batches:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    def mark_batch_expired(self, batch_id: int) -> bool:
        sql = """
        UPDATE MEDICINE_BATCH
        SET status = 'Expired',
            quantity_on_hand = 0
        WHERE batch_id = %s
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (batch_id,))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error marking batch expired:", e)
            return False
        finally:
            if cursor:
                cursor.close()

    def mark_batch_return_to_supplier(self, batch_id: int) -> bool:
        sql = """
        UPDATE MEDICINE_BATCH
        SET status = 'ReturnToSupplier'
        WHERE batch_id = %s
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (batch_id,))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error marking batch return to supplier:", e)
            return False
        finally:
            if cursor:
                cursor.close()

    # ---------- Prescription & Dispensing ----------

    def get_prescription_header(self, prescription_id: int) -> Optional[Dict]:
        sql = """
        SELECT pr.prescription_id,
               pr.appointment_id,
               pr.doctor_id,
               pr.status AS prescription_status,
               p.patient_id,
               p.full_name AS patient_name
        FROM PRESCRIPTION pr
        JOIN APPOINTMENT a ON pr.appointment_id = a.appointment_id
        JOIN PATIENT p ON a.patient_id = p.patient_id
        WHERE pr.prescription_id = %s
        """
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql, (prescription_id,))
            row = cursor.fetchone()
            return row
        except Exception as e:
            print("Error fetching prescription header:", e)
            return None
        finally:
            if cursor:
                cursor.close()

    def get_prescription_items(self, prescription_id: int) -> List[Dict]:
        sql = """
        SELECT pi.prescription_item_id,
               pi.medicine_id,
               m.medicine_name,
               pi.dosage,
               pi.frequency,
               pi.duration,
               pi.instructions
        FROM PRESCRIPTION_ITEM pi
        JOIN MEDICINE m ON pi.medicine_id = m.medicine_id
        WHERE pi.prescription_id = %s
        """
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql, (prescription_id,))
            return cursor.fetchall()
        except Exception as e:
            print("Error fetching prescription items:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    def get_available_batches_for_medicine(self, medicine_id: int) -> List[Dict]:
        sql = """
        SELECT batch_id,
               batch_number,
               expiry_date,
               quantity_on_hand,
               reorder_level,
               status
        FROM MEDICINE_BATCH
        WHERE medicine_id = %s
          AND status = 'Active'
          AND quantity_on_hand > 0
          AND expiry_date >= CURDATE()
        ORDER BY expiry_date
        """
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql, (medicine_id,))
            return cursor.fetchall()
        except Exception as e:
            print("Error fetching available batches:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    def dispense_medicine(
        self,
        prescription_item_id: int,
        batch_id: int,
        quantity: int,
        staff_id: int,
    ) -> bool:
        """
        Insert into DISPENSED_MEDICINE and reduce batch quantity.
        """
        # First get current batch qty
        get_sql = "SELECT quantity_on_hand FROM MEDICINE_BATCH WHERE batch_id = %s FOR UPDATE"
        insert_sql = """
        INSERT INTO DISPENSED_MEDICINE
        (prescription_item_id, batch_id, quantity_dispensed,
         dispensed_by_staff_id, dispensed_at)
        VALUES (%s, %s, %s, %s, NOW())
        """
        update_sql = """
        UPDATE MEDICINE_BATCH
        SET quantity_on_hand = quantity_on_hand - %s
        WHERE batch_id = %s
        """

        cursor = None
        try:
            cursor = self.conn.cursor()
            # Start transaction implicitly
            cursor.execute(get_sql, (batch_id,))
            row = cursor.fetchone()
            if not row:
                print("Batch not found.")
                return False

            current_qty = row[0]
            if current_qty < quantity:
                print("Insufficient quantity in batch.")
                return False

            # Insert dispensed record
            cursor.execute(
                insert_sql,
                (prescription_item_id, batch_id, quantity, staff_id),
            )

            # Update batch quantity
            cursor.execute(update_sql, (quantity, batch_id))

            self.conn.commit()
            return True

        except Exception as e:
            print("Error dispensing medicine:", e)
            self.conn.rollback()
            return False

        finally:
            if cursor:
                cursor.close()
