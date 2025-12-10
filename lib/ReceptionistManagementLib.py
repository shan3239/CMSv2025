from datetime import datetime
from dao.ReceptionistDaoImpl import ReceptionistDaoImpl
from validation.Receptionist_Validation import ReceptionistValidation


class ReceptionistManagementLib:

    dao = ReceptionistDaoImpl()

    # ✅ FIXED FUNCTION (WAS MISSING)
    @staticmethod
    def list_patients():
        print("\n--- Patient List ---")
        patients = ReceptionistManagementLib.dao.list_patients()
        if not patients:
            print("No patients found.")
            return

        for p in patients:
            print(
                f"ID: {p['patient_id']} | Name: {p['full_name']} | "
                f"Gender: {p['gender']} | Phone: {p['phone']} | "
                f"Blood: {p.get('blood_group')} | Membership: {p.get('membership_status')}"
            )

    # ---------- Patient Management ----------

    @staticmethod
    def register_patient():
        print("\n--- Register New Patient ---")

        # Full Name
        while True:
            full_name = input("Full Name: ").strip()
            if ReceptionistValidation.validate_full_name(full_name):
                break
            print("❌ Invalid name (min 3 letters, alphabets only)")

        # DOB
        while True:
            dob = input("Date of Birth (YYYY-MM-DD, optional): ").strip()
            if ReceptionistValidation.validate_dob(dob):
                dob = dob if dob else None
                break
            print("❌ Invalid DOB")

        # Gender
        while True:
            gender = input("Gender (M/F/O, optional): ").strip()
            if ReceptionistValidation.validate_gender(gender):
                break
            print("❌ Invalid Gender")

        # Phone
        while True:
            phone = input("Phone: ").strip()
            if ReceptionistValidation.validate_phone(phone):
                break
            print("❌ Phone must be 10 digits")

        # Email
        while True:
            email = input("Email (optional): ").strip()
            if ReceptionistValidation.validate_email(email):
                break
            print("❌ Invalid email format")

        address = input("Address (optional): ").strip()

        # Blood group
        while True:
            blood_group = input("Blood Group (A+, O-, optional): ").strip()
            if ReceptionistValidation.validate_blood_group(blood_group):
                blood_group = blood_group if blood_group else None
                break
            print("❌ Invalid blood group")

        # Height
        while True:
            h = input("Height in cm (optional): ").strip()
            if ReceptionistValidation.validate_height(h):
                height_cm = float(h) if h else None
                break
            print("❌ Invalid height")

        # Weight
        while True:
            w = input("Weight in kg (optional): ").strip()
            if ReceptionistValidation.validate_weight(w):
                weight_kg = float(w) if w else None
                break
            print("❌ Invalid weight")

        allergies = input("Allergies (optional): ").strip()
        past_conditions = input("Past Medical Conditions (optional): ").strip()

        # Membership
        while True:
            membership_status = input("Membership Status (Regular/Premium, optional): ").strip()
            if ReceptionistValidation.validate_membership(membership_status):
                membership_status = membership_status if membership_status else None
                break
            print("❌ Invalid membership type")

        patient_data = {
            "full_name": full_name,
            "dob": dob,
            "gender": gender,
            "phone": phone,
            "email": email if email else None,
            "address": address if address else None,
            "blood_group": blood_group,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "allergies": allergies if allergies else None,
            "past_medical_conditions": past_conditions if past_conditions else None,
            "membership_status": membership_status,
        }

        patient_id = ReceptionistManagementLib.dao.register_patient(patient_data)
        if patient_id:
            print(f"✅ Patient registered with ID: {patient_id}")
        else:
            print("❌ Failed")

    # ---------- Appointment ----------

    @staticmethod
    def schedule_appointment(receptionist_staff):

        print("\n--- Schedule Appointment ---")

        if input("View patient list? (y/n): ").lower() == "y":
            ReceptionistManagementLib.list_patients()

        # Patient ID
        while True:
            pid = input("Enter Patient ID: ").strip()
            if ReceptionistValidation.validate_patient_id(pid, ReceptionistManagementLib.dao):
                patient_id = int(pid)
                break
            print("❌ Invalid patient ID")

        patient = ReceptionistManagementLib.dao.get_patient_by_id(patient_id)
        print(f"Selected Patient: {patient['full_name']}")

        print("\nAvailable Doctors:")
        doctors = ReceptionistManagementLib.dao.list_doctors()
        if not doctors:
            print("No doctors available.")
            return

        for d in doctors:
            print(f"{d['doctor_id']} | {d['doctor_name']} | {d['specialization']} | {d['consultation_fee']}")

        # Doctor ID
        while True:
            did = input("Enter Doctor ID: ").strip()
            if ReceptionistValidation.validate_doctor_id(did, doctors):
                doctor_id = int(did)
                break
            print("❌ Invalid doctor")

        # Date Time
        while True:
            dt = input("Appointment Date & Time (YYYY-MM-DD HH:MM): ").strip()
            if ReceptionistValidation.validate_datetime(dt):
                dt_obj = datetime.strptime(dt, "%Y-%m-%d %H:%M")
                mysql_datetime = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
                break
            print("❌ Invalid datetime or past time")

        while True:
            reason = input("Reason for visit: ").strip()
            if ReceptionistValidation.validate_reason(reason):
                break
            print("❌ Invalid input (only letters allowed, no numbers or symbols)")


        appt_id = ReceptionistManagementLib.dao.schedule_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            scheduled_datetime=mysql_datetime,
            reason_for_visit=reason,
            created_by_staff_id=receptionist_staff.staff_id,
        )

        print(f"✅ Appointment created: {appt_id}" if appt_id else "❌ Failed")

    # ---------- VIEW APPOINTMENTS ----------

    @staticmethod
    def view_appointments_by_date():
        print("\n--- View Appointments ---")

        while True:
            date_str = input("Date (YYYY-MM-DD): ").strip()
            if ReceptionistValidation.validate_date(date_str):
                break
            print("❌ Invalid date")

        appts = ReceptionistManagementLib.dao.get_appointments_by_date(date_str)
        if not appts:
            print("No appointments.")
            return

        for a in appts:
            print(
                f"{a['appointment_id']} | {a['scheduled_datetime']} | "
                f"{a['patient_name']} | {a['doctor_name']} | {a['status']}"
            )

    # ---------- BILLING ----------

    @staticmethod
    def generate_consultation_bill():
        print("\n--- Generate Bill ---")

        while True:
            appt = input("Appointment ID: ").strip()
            if ReceptionistValidation.validate_appointment_id(appt):
                appointment_id = int(appt)
                break
            print("❌ Invalid appointment ID")

        bill_id = ReceptionistManagementLib.dao.create_consultation_bill(appointment_id)
        print(f"✅ Bill ID: {bill_id}" if bill_id else "❌ Failed")