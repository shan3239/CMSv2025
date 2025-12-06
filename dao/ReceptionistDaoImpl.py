from typing import List, Dict, Optional
from pymysql.cursors import DictCursor

from dao.AbstractReceptionistDao import ReceptionistDaoService
from DbConnection.ConnectionDB import ConnectionDB


class ReceptionistDaoImpl(ReceptionistDaoService):
    """
    DAO implementation for Receptionist use cases.
    """

    def __init__(self):
        self.conn = ConnectionDB().get_connection()

    # ---------- Patient Management ----------

    def register_patient(self, patient_data: Dict) -> Optional[int]:
        sql = """
        INSERT INTO PATIENT
        (full_name, dob, gender, phone, email, address,
         blood_group, height_cm, weight_kg, allergies,
         past_medical_conditions, membership_status, created_at)
        VALUES
        (%s, %s, %s, %s, %s, %s,
         %s, %s, %s, %s,
         %s, %s, NOW())
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                sql,
                (
                    patient_data.get("full_name"),
                    patient_data.get("dob"),
                    patient_data.get("gender"),
                    patient_data.get("phone"),
                    patient_data.get("email"),
                    patient_data.get("address"),
                    patient_data.get("blood_group"),
                    patient_data.get("height_cm"),
                    patient_data.get("weight_kg"),
                    patient_data.get("allergies"),
                    patient_data.get("past_medical_conditions"),
                    patient_data.get("membership_status"),
                ),
            )
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error registering patient:", e)
            return None
        finally:
            if cursor:
                cursor.close()

    def list_patients(self) -> List[Dict]:
        sql = """
        SELECT patient_id, full_name, gender, phone, email,
               blood_group, membership_status, created_at
        FROM PATIENT
        ORDER BY patient_id DESC
        """
        cursor = None
        patients = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql)
            patients = cursor.fetchall()
        except Exception as e:
            print("Error listing patients:", e)
        finally:
            if cursor:
                cursor.close()
        return patients

    def get_patient_by_id(self, patient_id: int) -> Optional[Dict]:
        sql = """
        SELECT *
        FROM PATIENT
        WHERE patient_id = %s
        """
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql, (patient_id,))
            row = cursor.fetchone()
            return row
        except Exception as e:
            print("Error fetching patient by ID:", e)
            return None
        finally:
            if cursor:
                cursor.close()

    # ---------- Doctor & Appointment Management ----------

    def list_doctors(self) -> List[Dict]:
        sql = """
        SELECT d.doctor_id,
               s.full_name AS doctor_name,
               d.specialization,
               d.consultation_fee,
               d.status
        FROM DOCTOR d
        JOIN STAFF s ON d.staff_id = s.staff_id
        WHERE d.status = 'Active'
        ORDER BY doctor_name
        """
        cursor = None
        doctors = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql)
            doctors = cursor.fetchall()
        except Exception as e:
            print("Error listing doctors:", e)
        finally:
            if cursor:
                cursor.close()
        return doctors

    def schedule_appointment(
        self,
        patient_id: int,
        doctor_id: int,
        scheduled_datetime: str,
        reason_for_visit: str,
        created_by_staff_id: int
    ) -> Optional[int]:
        sql = """
        INSERT INTO APPOINTMENT
        (patient_id, doctor_id, scheduled_datetime,
         status, reason_for_visit,
         created_by_staff_id, created_at)
        VALUES
        (%s, %s, %s,
         'Scheduled', %s,
         %s, NOW())
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                sql,
                (
                    patient_id,
                    doctor_id,
                    scheduled_datetime,
                    reason_for_visit,
                    created_by_staff_id,
                ),
            )
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error scheduling appointment:", e)
            return None
        finally:
            if cursor:
                cursor.close()

    def get_appointments_by_date(self, date_str: str) -> List[Dict]:
        sql = """
        SELECT a.appointment_id,
               a.scheduled_datetime,
               a.status,
               a.reason_for_visit,
               p.patient_id,
               p.full_name AS patient_name,
               d.doctor_id,
               s.full_name AS doctor_name
        FROM APPOINTMENT a
        JOIN PATIENT p ON a.patient_id = p.patient_id
        JOIN DOCTOR d ON a.doctor_id = d.doctor_id
        JOIN STAFF s ON d.staff_id = s.staff_id
        WHERE DATE(a.scheduled_datetime) = %s
        ORDER BY a.scheduled_datetime
        """
        cursor = None
        appts = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql, (date_str,))
            appts = cursor.fetchall()
        except Exception as e:
            print("Error fetching appointments by date:", e)
        finally:
            if cursor:
                cursor.close()
        return appts

    # ---------- Billing ----------

    def get_appointment_details(self, appointment_id: int) -> Optional[Dict]:
        sql = """
        SELECT a.appointment_id,
               a.patient_id,
               a.doctor_id,
               a.status AS appointment_status,
               a.scheduled_datetime,
               a.reason_for_visit,
               p.full_name AS patient_name,
               d.consultation_fee,
               s.full_name AS doctor_name
        FROM APPOINTMENT a
        JOIN PATIENT p ON a.patient_id = p.patient_id
        JOIN DOCTOR d ON a.doctor_id = d.doctor_id
        JOIN STAFF s ON d.staff_id = s.staff_id
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

    def create_consultation_bill(self, appointment_id: int) -> Optional[int]:
        """
        Creates a bill & bill_item using doctor's consultation_fee.
        """
        # Step 1: Get appointment & fee
        appt = self.get_appointment_details(appointment_id)
        if not appt:
            print("Appointment not found.")
            return None

        patient_id = appt["patient_id"]
        fee = appt["consultation_fee"]

        cursor = None
        try:
            cursor = self.conn.cursor()

            # Step 2: Insert into BILL
            bill_sql = """
            INSERT INTO BILL
            (patient_id, appointment_id, bill_type,
             total_amount, status, created_at)
            VALUES
            (%s, %s, 'Consultation', %s, 'Unpaid', NOW())
            """
            cursor.execute(bill_sql, (patient_id, appointment_id, fee))
            bill_id = cursor.lastrowid

            # Step 3: Insert into BILL_ITEM
            item_sql = """
            INSERT INTO BILL_ITEM
            (bill_id, item_type, reference_id, description,
             quantity, unit_price, amount)
            VALUES
            (%s, 'Consultation Fee', %s, %s,
             1, %s, %s)
            """
            description = "Consultation with Dr. " + appt["doctor_name"]
            cursor.execute(
                item_sql,
                (bill_id, appointment_id, description, fee, fee),
            )

            self.conn.commit()
            return bill_id

        except Exception as e:
            print("Error creating consultation bill:", e)
            return None

        finally:
            if cursor:
                cursor.close()
