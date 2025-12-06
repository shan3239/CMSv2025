from typing import List, Dict, Optional
from dao.AbstractDotorDao import DoctorDaoService
from DbConnection.ConnectionDB import ConnectionDB
from pymysql.cursors import DictCursor


class DoctorDaoImpl(DoctorDaoService):

    def __init__(self):
        self.conn = ConnectionDB().get_connection()

    def get_doctor_id_by_staff_id(self, staff_id: int) -> Optional[int]:
        sql = "SELECT doctor_id FROM DOCTOR WHERE staff_id = %s AND status = 'Active'"
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql, (staff_id,))
            row = cursor.fetchone()
            if row:
                return row["doctor_id"]
            return None
        except Exception as e:
            print("Error fetching doctor_id:", e)
            return None
        finally:
            if cursor:
                cursor.close()

    def get_appointments_for_doctor(self, doctor_id: int) -> List[Dict]:
        sql = """
        SELECT a.appointment_id, a.scheduled_datetime, a.status,
               p.patient_id, p.full_name AS patient_name, a.reason_for_visit
        FROM APPOINTMENT a
        JOIN PATIENT p ON a.patient_id = p.patient_id
        WHERE a.doctor_id = %s
        ORDER BY a.scheduled_datetime DESC
        """
        cursor = None
        appointments = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql, (doctor_id,))
            appointments = cursor.fetchall()
        except Exception as e:
            print("Error fetching appointments:", e)
        finally:
            if cursor:
                cursor.close()
        return appointments

    def get_appointment_details(self, appointment_id: int) -> Optional[Dict]:
        sql = """
        SELECT a.appointment_id, a.scheduled_datetime, a.status,
               a.reason_for_visit, p.patient_id, p.full_name AS patient_name,
               p.gender, p.dob, p.blood_group
        FROM APPOINTMENT a
        JOIN PATIENT p ON a.patient_id = p.patient_id
        WHERE a.appointment_id = %s
        """
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql, (appointment_id,))
            row = cursor.fetchone()
            return row
        except Exception as e:
            print("Error fetching appointment details:", e)
            return None
        finally:
            if cursor:
                cursor.close()

    def insert_consultation_note(self, appointment_id: int, doctor_id: int,
                                 symptoms: str, observations: str,
                                 diagnosis: str, recommendations: str) -> bool:
        sql = """
        INSERT INTO CONSULTATION_NOTE
        (appointment_id, doctor_id, symptoms, observations, diagnosis, recommendations)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (appointment_id, doctor_id, symptoms,
                                 observations, diagnosis, recommendations))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting consultation note:", e)
            return False
        finally:
            if cursor:
                cursor.close()

    def create_prescription(self, appointment_id: int, doctor_id: int) -> Optional[int]:
        sql = """
        INSERT INTO PRESCRIPTION (appointment_id, doctor_id, status)
        VALUES (%s, %s, 'Active')
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (appointment_id, doctor_id))
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error creating prescription:", e)
            return None
        finally:
            if cursor:
                cursor.close()

    def add_prescription_item(self, prescription_id: int, medicine_id: int,
                              dosage: str, frequency: str,
                              duration: str, instructions: str) -> bool:
        sql = """
        INSERT INTO PRESCRIPTION_ITEM
        (prescription_id, medicine_id, dosage, frequency, duration, instructions)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (prescription_id, medicine_id,
                                 dosage, frequency, duration, instructions))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting prescription item:", e)
            return False
        finally:
            if cursor:
                cursor.close()

    def list_medicines(self) -> List[Dict]:
        sql = """
        SELECT medicine_id, medicine_name, category, form, strength, status
        FROM MEDICINE
        WHERE status = 'Active'
        ORDER BY medicine_name
        """
        cursor = None
        meds = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql)
            meds = cursor.fetchall()
        except Exception as e:
            print("Error fetching medicines:", e)
        finally:
            if cursor:
                cursor.close()
        return meds

    def create_lab_order(self, appointment_id: int, patient_id: int,
                         doctor_id: int, notes: str) -> Optional[int]:
        sql = """
        INSERT INTO LAB_ORDER (appointment_id, patient_id, doctor_id, status, notes)
        VALUES (%s, %s, %s, 'Pending', %s)
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (appointment_id, patient_id, doctor_id, notes))
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error creating lab order:", e)
            return None
        finally:
            if cursor:
                cursor.close()

    def add_lab_order_item(self, lab_order_id: int, lab_test_id: int,
                           notes: str) -> bool:
        sql = """
        INSERT INTO LAB_ORDER_ITEM (lab_order_id, lab_test_id, notes)
        VALUES (%s, %s, %s)
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (lab_order_id, lab_test_id, notes))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting lab order item:", e)
            return False
        finally:
            if cursor:
                cursor.close()

    def list_lab_tests(self) -> List[Dict]:
        sql = """
        SELECT lab_test_id, test_name, category, description, normal_range, units, status
        FROM LAB_TEST
        WHERE status = 'Active'
        ORDER BY test_name
        """
        cursor = None
        tests = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql)
            tests = cursor.fetchall()
        except Exception as e:
            print("Error fetching lab tests:", e)
        finally:
            if cursor:
                cursor.close()
        return tests

    def get_patient_medical_history(self, patient_id: int) -> Dict:
        result = {
            "appointments": [],
            "consultations": [],
            "prescriptions": [],
            "lab_results": []
        }
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)

            # Appointments
            cursor.execute("""
                SELECT a.appointment_id, a.scheduled_datetime, a.status,
                       a.reason_for_visit, d.doctor_id, s.full_name AS doctor_name
                FROM APPOINTMENT a
                JOIN DOCTOR d ON a.doctor_id = d.doctor_id
                JOIN STAFF s ON d.staff_id = s.staff_id
                WHERE a.patient_id = %s
                ORDER BY a.scheduled_datetime DESC
            """, (patient_id,))
            result["appointments"] = cursor.fetchall()

            # Consultation notes
            cursor.execute("""
                SELECT c.consultation_id, c.appointment_id, c.symptoms,
                       c.observations, c.diagnosis, c.recommendations, c.created_at
                FROM CONSULTATION_NOTE c
                JOIN APPOINTMENT a ON c.appointment_id = a.appointment_id
                WHERE a.patient_id = %s
                ORDER BY c.created_at DESC
            """, (patient_id,))
            result["consultations"] = cursor.fetchall()

            # Prescriptions
            cursor.execute("""
                SELECT pr.prescription_id, pr.appointment_id, pr.status, pr.created_at
                FROM PRESCRIPTION pr
                JOIN APPOINTMENT a ON pr.appointment_id = a.appointment_id
                WHERE a.patient_id = %s
                ORDER BY pr.created_at DESC
            """, (patient_id,))
            result["prescriptions"] = cursor.fetchall()

            # Lab results
            cursor.execute("""
                SELECT lr.result_id, lo.lab_order_id, lt.test_name,
                       lr.result_value, lr.units, lr.result_date, lr.comments
                FROM LAB_RESULT lr
                JOIN LAB_ORDER_ITEM loi ON lr.lab_order_item_id = loi.lab_order_item_id
                JOIN LAB_ORDER lo ON loi.lab_order_id = lo.lab_order_id
                JOIN LAB_TEST lt ON loi.lab_test_id = lt.lab_test_id
                WHERE lo.patient_id = %s
                ORDER BY lr.result_date DESC
            """, (patient_id,))
            result["lab_results"] = cursor.fetchall()

        except Exception as e:
            print("Error fetching medical history:", e)
        finally:
            if cursor:
                cursor.close()
        return result

    def insert_patient_vitals(self, appointment_id: int, staff_id: int,
                              bp: str, temp: float,
                              pulse: int, spo2: int,
                              rr: int) -> bool:
        sql = """
        INSERT INTO PATIENT_VITALS
        (appointment_id, recorded_by_staff_id, blood_pressure,
         temperature, pulse, spo2, respiratory_rate)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (appointment_id, staff_id, bp,
                                 temp, pulse, spo2, rr))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting vitals:", e)
            return False
        finally:
            if cursor:
                cursor.close()

    def get_lab_results_for_doctor(self, doctor_id: int) -> List[Dict]:
        sql = """
        SELECT lr.result_id, lo.lab_order_id, lt.test_name,
               lr.result_value, lr.units, lr.result_date, lr.comments,
               p.full_name AS patient_name
        FROM LAB_RESULT lr
        JOIN LAB_ORDER_ITEM loi ON lr.lab_order_item_id = loi.lab_order_item_id
        JOIN LAB_ORDER lo ON loi.lab_order_id = lo.lab_order_id
        JOIN LAB_TEST lt ON loi.lab_test_id = lt.lab_test_id
        JOIN PATIENT p ON lo.patient_id = p.patient_id
        WHERE lo.doctor_id = %s
        ORDER BY lr.result_date DESC
        """
        cursor = None
        results = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql, (doctor_id,))
            results = cursor.fetchall()
        except Exception as e:
            print("Error fetching lab results:", e)
        finally:
            if cursor:
                cursor.close()
        return results

    def update_diagnosis(self, consultation_id: int, new_diagnosis: str) -> bool:
        sql = "UPDATE CONSULTATION_NOTE SET diagnosis = %s WHERE consultation_id = %s"
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (new_diagnosis, consultation_id))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error updating diagnosis:", e)
            return False
        finally:
            if cursor:
                cursor.close()

    def create_followup_appointment(self, old_appointment_id: int,
                                    new_datetime: str,
                                    reason: str) -> bool:
        # Copy patient_id and doctor_id from old appointment
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute("""
                SELECT patient_id, doctor_id
                FROM APPOINTMENT
                WHERE appointment_id = %s
            """, (old_appointment_id,))
            row = cursor.fetchone()
            if not row:
                print("Old appointment not found.")
                return False

            patient_id = row["patient_id"]
            doctor_id = row["doctor_id"]

            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO APPOINTMENT
                (patient_id, doctor_id, scheduled_datetime, status, reason_for_visit, created_by_staff_id)
                VALUES (%s, %s, %s, 'Scheduled', %s, NULL)
            """, (patient_id, doctor_id, new_datetime, reason))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error creating follow-up appointment:", e)
            return False
        finally:
            if cursor:
                cursor.close()
