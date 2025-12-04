from Dao.AdminDao import AdminDao
from models.Staff import Staff
from Validation.AdminValidation import AdminValidation

adminDao = AdminDao()

def admin_menu():
    while True:
        print("\n========== ADMIN PANEL ==========")
        print("1. Create Staff")
        print("2. Update Staff")
        print("3. Deactivate Staff")
        print("4. View All Staff")
        print("5. View System Audit Logs")
        print("6. View Roles")
        print("0. Logout")

        choice = input("Select an option: ")

        if choice == "1":
            create_staff_ui()

        elif choice == "2":
            update_staff_ui()

        elif choice == "3":
            staff_id = input("Enter Staff ID to deactivate: ")
            adminDao.deactivate_staff(staff_id)
            print("Staff deactivated.")

        elif choice == "4":
            staff_list = adminDao.list_staff()
            print("\n---- STAFF LIST ----")
            for user in staff_list:
                print(user)

        elif choice == "5":
            logs = adminDao.view_audit_logs()
            print("\n---- AUDIT LOGS ----")
            for log in logs:
                print(log)

        elif choice == "6":
            roles = adminDao.list_roles()
            print("\n---- ROLES ----")
            for r in roles:
                print(r)

        elif choice == "0":
            print("Logging out...")
            break

        else:
            print("Invalid choice. Try again.")


# ---------------- UI FUNCTIONS ---------------- #

def create_staff_ui():
    print("\n--- Create New Staff ---")
    full_name = input("Full Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    username = input("Username: ")
    password = input("Password: ")
    role_id = input("Role ID: ")

    staff = Staff(full_name=full_name, email=email, phone=phone,
                  username=username, password_hash=password, role_id=role_id)

    is_valid, msg = AdminValidation.validate_staff_data(staff)
    if not is_valid:
        print("Error:", msg)
        return

    count, staff_id = adminDao.create_staff(staff)
    print(f"Staff created successfully with ID: {staff_id}")


def update_staff_ui():
    print("\n--- Update Staff ---")
    staff_id = input("Staff ID: ")
    full_name = input("Full Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    role_id = input("Role ID: ")
    status = input("Status (Active/Inactive): ")

    result = adminDao.update_staff(staff_id, full_name, email, phone, role_id, status)
    print("Updated successfully." if result else "No changes made.")


# ---------------- ENTRY POINT ---------------- #

if __name__ == "__main__":
    print("Admin logged in successfully.")
    admin_menu()
