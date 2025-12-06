from dao.DoctorDaoImpl import DoctorDaoImpl
from models.staff import Staff


class DoctorManagementLib:
    """
    Handles doctor use cases for console UI
    """

    dao = DoctorDaoImpl()

    @staticmethod
    def get_doctor_id_for_user(user: Staff) -> int:
        doctor_id = DoctorManagementLib.dao.get_doctor_id_by_staff_id(user.staff_id)
        if not doctor_id:
            print("❌ No doctor profile linked to this user.")
            return None
        return doctor_id

    @staticmethod
    def view_my_appointments(user: Staff):
        doctor_id = DoctorManagementLib.get_doctor_id_for_user(user)
        if not doctor_id:
            return

        appts = DoctorManagementLib.dao.get_appointments_for_doctor(doctor_id)
        if not appts:
            print("No appointments found.")
            return

        print("\n--- My Appointments ---")
        for a in appts:
            print(
                f"ID: {a['appointment_id']}, DateTime: {a['scheduled_datetime']}, "
                f"Patient: {a['patient_name']}, Status: {a['status']}, "
                f"Reason: {a['reason_for_visit']}"
            )

    @staticmethod
    def record_consultation_notes(user: Staff):
        doctor_id = DoctorManagementLib.get_doctor_id_for_user(user)
        if not doctor_id:
            return

        appt_id = input("Enter Appointment ID: ").strip()
        if not appt_id.isdigit():
            print("Invalid appointment ID.")
            return
        appt_id = int(appt_id)

        details = DoctorManagementLib.dao.get_appointment_details(appt_id)
        if not details:
            print("Appointment not found.")
            return

        print(f"\nRecording notes for Patient: {details['patient_name']} (Appt ID: {appt_id})")

        symptoms = input("Symptoms: ")
        observations = input("Observations: ")
        diagnosis = input("Diagnosis: ")
        recommendations = input("Recommendations: ")

        if DoctorManagementLib.dao.insert_consultation_note(
            appt_id, doctor_id, symptoms, observations, diagnosis, recommendations
        ):
            print("✅ Consultation notes saved.")
        else:
            print("❌ Failed to save consultation notes.")

    @staticmethod
    def prescribe_medication(user: Staff):
        doctor_id = DoctorManagementLib.get_doctor_id_for_user(user)
        if not doctor_id:
            return

        appt_id = input("Enter Appointment ID: ").strip()
        if not appt_id.isdigit():
            print("Invalid appointment ID.")
            return
        appt_id = int(appt_id)

        prescription_id = DoctorManagementLib.dao.create_prescription(appt_id, doctor_id)
        if not prescription_id:
            print("❌ Could not create prescription.")
            return

        print(f"✅ New Prescription ID: {prescription_id}")

        # List medicines
        meds = DoctorManagementLib.dao.list_medicines()
        if not meds:
            print("No medicines available.")
            return

        print("\nAvailable Medicines:")
        for m in meds:
            print(
                f"{m['medicine_id']}: {m['medicine_name']} ({m['strength']}) - {m['category']}"
            )

        while True:
            med_id = input("\nEnter Medicine ID to add (or 0 to finish): ").strip()
            if med_id == "0":
                break
            if not med_id.isdigit():
                print("Invalid ID.")
                continue

            med_id = int(med_id)
            dosage = input("Dosage (e.g., 500mg): ")
            frequency = input("Frequency (e.g., 2 times/day): ")
            duration = input("Duration (e.g., 5 days): ")
            instructions = input("Instructions (e.g., After food): ")

            if DoctorManagementLib.dao.add_prescription_item(
                prescription_id, med_id, dosage, frequency, duration, instructions
            ):
                print("✅ Medicine added to prescription.")
            else:
                print("❌ Failed to add medicine.")

        print("Prescription completed.")

    @staticmethod
    def prescribe_lab_tests(user: Staff):
        doctor_id = DoctorManagementLib.get_doctor_id_for_user(user)
        if not doctor_id:
            return

        appt_id = input("Enter Appointment ID: ").strip()
        if not appt_id.isdigit():
            print("Invalid appointment ID.")
            return
        appt_id = int(appt_id)

        details = DoctorManagementLib.dao.get_appointment_details(appt_id)
        if not details:
            print("Appointment not found.")
            return
        patient_id = details["patient_id"]

        notes = input("General notes for lab order: ")
        lab_order_id = DoctorManagementLib.dao.create_lab_order(appt_id, patient_id, doctor_id, notes)
        if not lab_order_id:
            print("❌ Failed to create lab order.")
            return

        tests = DoctorManagementLib.dao.list_lab_tests()
        if not tests:
            print("No lab tests available.")
            return

        print("\nAvailable Lab Tests:")
        for t in tests:
            print(f"{t['lab_test_id']}: {t['test_name']} ({t['category']})")

        while True:
            test_id = input("\nEnter Lab Test ID to add (or 0 to finish): ").strip()
            if test_id == "0":
                break
            if not test_id.isdigit():
                print("Invalid ID.")
                continue
            test_id = int(test_id)
            note = input("Notes for this test: ")

            if DoctorManagementLib.dao.add_lab_order_item(lab_order_id, test_id, note):
                print("✅ Lab test added.")
            else:
                print("❌ Failed to add lab test.")

        print("Lab order completed.")

    @staticmethod
    def view_patient_history():
        pid = input("Enter Patient ID: ").strip()
        if not pid.isdigit():
            print("Invalid patient ID.")
            return
        pid = int(pid)

        history = DoctorManagementLib.dao.get_patient_medical_history(pid)

        print("\n--- Appointments ---")
        for a in history["appointments"]:
            print(
                f"ApptID: {a['appointment_id']}, Date: {a['scheduled_datetime']}, "
                f"Doctor: {a['doctor_name']}, Reason: {a['reason_for_visit']}, Status: {a['status']}"
            )

        print("\n--- Consultations ---")
        for c in history["consultations"]:
            print(
                f"ConsID: {c['consultation_id']}, ApptID: {c['appointment_id']}, "
                f"Diagnosis: {c['diagnosis']}, Date: {c['created_at']}"
            )

        print("\n--- Prescriptions ---")
        for p in history["prescriptions"]:
            print(
                f"PresID: {p['prescription_id']}, ApptID: {p['appointment_id']}, "
                f"Status: {p['status']}, Date: {p['created_at']}"
            )

        print("\n--- Lab Results ---")
        for r in history["lab_results"]:
            print(
                f"ResultID: {r['result_id']}, Test: {r['test_name']}, "
                f"Value: {r['result_value']} {r['units']}, Date: {r['result_date']}"
            )

    @staticmethod
    def record_patient_vitals(user: Staff):
        doctor_id = DoctorManagementLib.get_doctor_id_for_user(user)
        if not doctor_id:
            return

        appt_id = input("Enter Appointment ID: ").strip()
        if not appt_id.isdigit():
            print("Invalid appointment ID.")
            return
        appt_id = int(appt_id)

        bp = input("Blood Pressure (e.g., 120/80): ")
        try:
            temp = float(input("Temperature (e.g., 98.6): "))
        except ValueError:
            print("Invalid temperature.")
            return

        try:
            pulse = int(input("Pulse: "))
            spo2 = int(input("SpO2 (%): "))
            rr = int(input("Respiratory Rate: "))
        except ValueError:
            print("Pulse, SpO2 and RR must be numbers.")
            return

        if DoctorManagementLib.dao.insert_patient_vitals(appt_id, user.staff_id, bp, temp, pulse, spo2, rr):
            print("✅ Vitals recorded.")
        else:
            print("❌ Failed to record vitals.")

    @staticmethod
    def review_lab_results(user: Staff):
        doctor_id = DoctorManagementLib.get_doctor_id_for_user(user)
        if not doctor_id:
            return

        results = DoctorManagementLib.dao.get_lab_results_for_doctor(doctor_id)
        if not results:
            print("No lab results found.")
            return

        print("\n--- Lab Results for My Patients ---")
        for r in results:
            print(
                f"ResultID: {r['result_id']}, Patient: {r['patient_name']}, "
                f"Test: {r['test_name']}, Value: {r['result_value']} {r['units']}, "
                f"Date: {r['result_date']}, Comments: {r['comments']}"
            )

    @staticmethod
    def update_diagnosis():
        cons_id = input("Enter Consultation ID to update: ").strip()
        if not cons_id.isdigit():
            print("Invalid Consultation ID.")
            return
        cons_id = int(cons_id)

        new_diag = input("Enter new Diagnosis: ")

        if DoctorManagementLib.dao.update_diagnosis(cons_id, new_diag):
            print("✅ Diagnosis updated.")
        else:
            print("❌ Failed to update diagnosis.")

    @staticmethod
    def recommend_followup():
        old_appt_id = input("Enter existing Appointment ID: ").strip()
        if not old_appt_id.isdigit():
            print("Invalid Appointment ID.")
            return
        old_appt_id = int(old_appt_id)

        new_dt = input("Enter follow-up date & time (YYYY-MM-DD HH:MM:SS): ")
        reason = input("Reason for follow-up: ")

        if DoctorManagementLib.dao.create_followup_appointment(old_appt_id, new_dt, reason):
            print("✅ Follow-up appointment created.")
        else:
            print("❌ Failed to create follow-up appointment.")
