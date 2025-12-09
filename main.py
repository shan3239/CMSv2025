from lib.AuthLib import AuthLib
from lib.AdminManagementLib import AdminManagementLib
from lib.ReceptionistManagementLib import ReceptionistManagementLib
from lib.PharmacistManagementLib import PharmacistManagementLib
from lib.LabTechnicianManagementLib import LabTechnicianManagementLib
from lib.DoctorManagementLib import DoctorManagementLib


# from lib.DoctorManagementLib import DoctorManagementLib  # when you implement doctor logic


def admin_menu(user):
    """
    Admin-only menu (Manage staff, roles, departments, logs)
    """
    while True:
        print("\n" + "=" * 70)
        print(f"   ADMIN MANAGEMENT MENU  (Logged in as: {user.full_name})")
        print("=" * 70)
        print("""
1. Create Staff
2. List All Staff
3. View Staff By ID
4. Update Staff (Single Field)
5. Deactivate Staff
6. Delete Staff
7. View Roles
8. View Departments
9. View Audit Logs
0. Logout
        """)
        choice = input("Enter choice: ").strip()

        if choice == "1":
            AdminManagementLib.create_staff()
        elif choice == "2":
            AdminManagementLib.list_staff()
        elif choice == "3":
            AdminManagementLib.view_staff_by_id()
        elif choice == "4":
            AdminManagementLib.update_staff()
        elif choice == "5":
            AdminManagementLib.deactivate_staff()
        elif choice == "6":
            AdminManagementLib.delete_staff()
        elif choice == "7":
            AdminManagementLib.view_roles()
        elif choice == "8":
            AdminManagementLib.view_departments()
        elif choice == "9":
            AdminManagementLib.view_audit_logs()
        elif choice == "0":
            print("Logging out from Admin...")
            break
        else:
            print("Invalid choice. Try again.")


def doctor_menu(user):
    """
    Doctor-only menu (placeholder for now)
    """
    while True:
        print("\n" + "=" * 70)
        print(f"         DOCTOR MENU  (Logged in as: {user.full_name})")
        print("=" * 70)
        print("""
1. View My Appointments
2. Record Consultation Notes
3. Prescribe Medication
4. Prescribe Lab Tests
5. View Patient Medical History
6. Record Patient Vitals
7. Review Lab Test Results
8. Recommend Follow-Up Appointment
9. Update Diagnosis
0. Logout
        """)
        choice = input("Enter choice: ").strip()

        if choice == "0":
            print("Logging out from Doctor...")
            break
        elif choice == "1":
            DoctorManagementLib.view_my_appointments(user)
        elif choice == "2":
            DoctorManagementLib.record_consultation_notes(user)

        elif choice == "3":
            DoctorManagementLib.prescribe_medication(user)

        elif choice == "4":
            DoctorManagementLib.prescribe_lab_tests(user)

        elif choice == "5":
            DoctorManagementLib.view_patient_history()

        elif choice == "6":
            DoctorManagementLib.record_patient_vitals(user)

        elif choice == "7":
            DoctorManagementLib.review_lab_results(user)

        elif choice == "8":
            DoctorManagementLib.recommend_followup()

        elif choice == "9":
            DoctorManagementLib.update_diagnosis()

        else:
            print("Doctor features not implemented yet in this version.")


def receptionist_menu(user):
    """
    Receptionist menu (uses ReceptionistManagementLib)
    """
    while True:
        print("\n" + "=" * 70)
        print(f"         RECEPTIONIST MENU  (Logged in as: {user.full_name})")
        print("=" * 70)
        print("""
1. Register New Patient
2. List Patients
3. Schedule Appointment
4. View Appointments by Date
5. Generate Consultation Billing
0. Logout
        """)
        choice = input("Enter choice: ").strip()

        if choice == "1":
            ReceptionistManagementLib.register_patient()
        elif choice == "2":
            ReceptionistManagementLib.list_patients()
        elif choice == "3":
            ReceptionistManagementLib.schedule_appointment(user)
        elif choice == "4":
            ReceptionistManagementLib.view_appointments_by_date()
        elif choice == "5":
            ReceptionistManagementLib.generate_consultation_bill()
        elif choice == "0":
            print("Logging out Receptionist...")
            break
        else:
            print("Invalid choice. Try again.")


def staff_login_menu():
    """
    Staff login options: Admin, Receptionist, Pharmacist, Lab Technician
    """
    while True:
        print("\n" + "=" * 70)
        print("                       STAFF LOGIN")
        print("=" * 70)
        print("""
1. Admin Login
2. Receptionist Login
3. Pharmacist Login
4. Lab Technician Login
0. Back to Main Menu
        """)
        choice = input("Enter choice: ").strip()

        if choice == "0":
            break

        username = input("Username: ").strip()
        password = input("Password: ").strip()

        user = AuthLib.login(username, password)
        if not user:
            print("Invalid login. Try again.")
            continue

        role = user.role_name.strip().lower()

        # Admin
        if choice == "1" and role in ("administrator", "admin"):
            admin_menu(user)

        # Receptionist
        elif choice == "2" and role == "receptionist":
            receptionist_menu(user)

        # Pharmacist
        elif choice == "3" and role == "pharmacist":
            pharmacist_menu(user)


        # Lab Technician
        elif choice == "4" and role == "lab technician":
            lab_technician_menu(user)


        else:
            print(f"Access denied. Wrong user role: {user.role_name}")

        print("\nReturning to Staff Login Menu...")


def main():
    print("*" * 80)
    print("        WELCOME TO CLINIC MANAGEMENT SYSTEM (CONSOLE VERSION)")
    print("*" * 80)

    while True:
        print("\n" + "=" * 70)
        print("                         MAIN MENU")
        print("=" * 70)
        print("""
1. Doctor Login
2. Staff Login (Admin / Receptionist / Pharmacist / Lab Technician)
0. Exit
        """)
        choice = input("Enter choice: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            user = AuthLib.login(username, password)
            if user and user.role_name.strip().lower() == "doctor":
                doctor_menu(user)
            else:
                print("Invalid doctor login or wrong role.")

        elif choice == "2":
            staff_login_menu()

        elif choice == "0":
            print("Exiting application... Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

def pharmacist_menu(user):
    """
    Pharmacist menu (uses PharmacistManagementLib)
    """
    while True:
        print("\n" + "=" * 70)
        print(f"         PHARMACIST MENU  (Logged in as: {user.full_name})")
        print("=" * 70)
        print("""
1. View Medicine Inventory
2. Add New Medicine
3. Add Medicine Batch
4. View Low Stock Batches
5. View Near-Expiry Batches
6. View Expired Batches
7. Mark Expired Batch (Remove from Stock)
8. Mark Batch as Return To Supplier
9. Dispense Medication (By Prescription)
0. Logout
        """)
        choice = input("Enter choice: ").strip()

        if choice == "1":
            PharmacistManagementLib.view_medicine_inventory()
        elif choice == "2":
            PharmacistManagementLib.add_medicine()
        elif choice == "3":
            PharmacistManagementLib.add_medicine_batch()
        elif choice == "4":
            PharmacistManagementLib.view_low_stock()
        elif choice == "5":
            PharmacistManagementLib.view_near_expiry()
        elif choice == "6":
            PharmacistManagementLib.view_expired()
        elif choice == "7":
            PharmacistManagementLib.remove_expired_batch()
        elif choice == "8":
            PharmacistManagementLib.mark_return_to_supplier()
        elif choice == "9":
            PharmacistManagementLib.dispense_medication(user)
        elif choice == "0":
            print("Logging out Pharmacist...")
            break
        else:
            print("Invalid choice. Try again.")

def lab_technician_menu(user):
    """
    Lab Technician menu (uses LabTechnicianManagementLib)
    """
    while True:
        print("\n" + "=" * 70)
        print(f"      LAB TECHNICIAN MENU  (Logged in as: {user.full_name})")
        print("=" * 70)
        print("""
1. List Lab Tests
2. Add Lab Test
3. Update Lab Test
4. View Pending Lab Orders
5. Record Lab Test Results
0. Logout
        """)
        choice = input("Enter choice: ").strip()

        if choice == "1":
            LabTechnicianManagementLib.list_lab_tests()
        elif choice == "2":
            LabTechnicianManagementLib.add_lab_test()
        elif choice == "3":
            LabTechnicianManagementLib.update_lab_test()
        elif choice == "4":
            LabTechnicianManagementLib.view_pending_lab_orders()
        elif choice == "5":
            LabTechnicianManagementLib.record_lab_results(user)
        elif choice == "0":
            print("Logging out Lab Technician...")
            break
        else:
            print("Invalid choice. Try again.")



if __name__ == "__main__":
    main()
