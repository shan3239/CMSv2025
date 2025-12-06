from datetime import datetime
from dao.ReceptionistDaoImpl import ReceptionistDaoImpl


class ReceptionistManagementLib:
    """
    Console logic for Receptionist use cases:
    - Register patient
    - List patients
    - Schedule appointment
    - View appointments by date
    - Generate consultation billing
    """

    dao = ReceptionistDaoImpl()

    # ---------- Patient Management ----------

    @staticmethod
    def register_patient():
        print("\n--- Register New Patient ---")

        # Basic required fields with simple validation loops

        # Full Name
        while True:
            full_name = input("Full Name: ").strip()
            if len(full_name) < 3:
                print("Error: Name must be at least 3 characters.")
            else:
                break

        dob = input("Date of Birth (YYYY-MM-DD, optional): ").strip()
        if dob == "":
            dob = None

        gender = input("Gender (M/F/O, optional): ").strip()

        # Phone
        while True:
            phone = input("Phone: ").strip()
            if not phone:
                print("Error: Phone is required.")
            else:
                break

        email = input("Email (optional): ").strip()
        address = input("Address (optional): ").strip()

        blood_group = input("Blood Group (e.g., A+, O-, optional): ").strip()

        # Height & Weight
        height_cm = None
        weight_kg = None

        h = input("Height in cm (optional): ").strip()
        if h:
            try:
                height_cm = float(h)
            except ValueError:
                print("Warning: Invalid height, ignoring.")

        w = input("Weight in kg (optional): ").strip()
        if w:
            try:
                weight_kg = float(w)
            except ValueError:
                print("Warning: Invalid weight, ignoring.")

        allergies = input("Allergies (optional): ").strip()
        past_conditions = input("Past Medical Conditions (optional): ").strip()
        membership_status = input("Membership Status (e.g., Regular/Premium, optional): ").strip()

        patient_data = {
            "full_name": full_name,
            "dob": dob,
            "gender": gender,
            "phone": phone,
            "email": email if email else None,
            "address": address if address else None,
            "blood_group": blood_group if blood_group else None,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "allergies": allergies if allergies else None,
            "past_medical_conditions": past_conditions if past_conditions else None,
            "membership_status": membership_status if membership_status else None,
        }

        patient_id = ReceptionistManagementLib.dao.register_patient(patient_data)
        if patient_id:
            print(f"✅ Patient registered successfully with ID: {patient_id}")
        else:
            print("❌ Failed to register patient.")

    @staticmethod
    def list_patients():
        print("\n--- Patient List ---")
        patients = ReceptionistManagementLib.dao.list_patients()
        if not patients:
            print("No patients found.")
            return
        for p in patients:
            print(
                f"ID: {p['patient_id']}, Name: {p['full_name']}, "
                f"Gender: {p['gender']}, Phone: {p['phone']}, "
                f"Blood: {p['blood_group']}, Membership: {p['membership_status']}"
            )

    # ---------- Appointment Management ----------

    @staticmethod
    def schedule_appointment(receptionist_staff):
        """
        receptionist_staff: Staff object of logged-in receptionist (for created_by_staff_id)
        """
        print("\n--- Schedule Appointment ---")

        # List patients (optional)
        show_patients = input("Do you want to see patient list? (y/n): ").strip().lower()
        if show_patients == "y":
            ReceptionistManagementLib.list_patients()

        # Patient ID
        while True:
            pid = input("Enter Patient ID: ").strip()
            if not pid.isdigit():
                print("Error: Patient ID must be a number.")
                continue
            patient_id = int(pid)
            patient = ReceptionistManagementLib.dao.get_patient_by_id(patient_id)
            if not patient:
                print("No patient found with that ID.")
                continue
            print(f"Selected Patient: {patient['full_name']}")
            break

        # List doctors
        print("\nAvailable Doctors:")
        doctors = ReceptionistManagementLib.dao.list_doctors()
        if not doctors:
            print("No active doctors found. Cannot create appointment.")
            return
        for d in doctors:
            print(
                f"Doctor ID: {d['doctor_id']}, Name: {d['doctor_name']}, "
                f"Spec: {d['specialization']}, Fee: {d['consultation_fee']}"
            )

        # Doctor ID
        while True:
            did = input("Enter Doctor ID: ").strip()
            if not did.isdigit():
                print("Error: Doctor ID must be a number.")
                continue
            doctor_id = int(did)
            if not any(d["doctor_id"] == doctor_id for d in doctors):
                print("Invalid Doctor ID from list.")
                continue
            break

        # Date & Time
        while True:
            dt_str = input("Enter Appointment Date & Time (YYYY-MM-DD HH:MM): ").strip()
            try:
                dt_obj = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
                mysql_datetime = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
                break
            except ValueError:
                print("Error: Invalid date-time format. Try again.")

        reason = input("Reason for visit: ").strip()

        appt_id = ReceptionistManagementLib.dao.schedule_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            scheduled_datetime=mysql_datetime,
            reason_for_visit=reason,
            created_by_staff_id=receptionist_staff.staff_id,
        )

        if appt_id:
            print(f"✅ Appointment scheduled successfully with ID: {appt_id}")
        else:
            print("❌ Failed to schedule appointment.")

    @staticmethod
    def view_appointments_by_date():
        print("\n--- View Appointments by Date ---")
        while True:
            date_str = input("Enter Date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Error: Invalid date format. Try again.")

        appts = ReceptionistManagementLib.dao.get_appointments_by_date(date_str)
        if not appts:
            print("No appointments found for that date.")
            return

        print(f"\nAppointments on {date_str}:")
        for a in appts:
            print(
                f"Appt ID: {a['appointment_id']}, Time: {a['scheduled_datetime']}, "
                f"Status: {a['status']}, Patient: {a['patient_name']} (ID: {a['patient_id']}), "
                f"Doctor: {a['doctor_name']} (ID: {a['doctor_id']}), "
                f"Reason: {a['reason_for_visit']}"
            )

    # ---------- Billing ----------

    @staticmethod
    def generate_consultation_bill():
        print("\n--- Generate Consultation Billing ---")

        while True:
            appt_str = input("Enter Appointment ID: ").strip()
            if not appt_str.isdigit():
                print("Error: Appointment ID must be a number.")
                continue
            appointment_id = int(appt_str)
            break

        bill_id = ReceptionistManagementLib.dao.create_consultation_bill(appointment_id)
        if bill_id:
            print(f"✅ Bill created successfully with Bill ID: {bill_id}")
        else:
            print("❌ Failed to create bill. Check appointment ID or data.")
