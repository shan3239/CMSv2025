from dao.AdminDaoImpl import AdminDaoImpl
from models.staff import Staff
from validation.staff_validations import (
    validate_staff_name,
    validate_username,
    validate_role_id,
    validate_email,
)


class AdminManagementLib:
    """
    Handles Admin operations: manage staff, roles, departments, audit logs
    """

    admin_service = AdminDaoImpl()

    @staticmethod
    def create_staff():
        print("\n--- Create New Staff ---")

        # Full Name
        while True:
            full_name = input("Full Name: ")
            try:
                validate_staff_name(full_name)
                break
            except Exception as e:
                print("Error:", e)

        # Email
        while True:
            email = input("Email: ")
            try:
                validate_email(email)
                break
            except Exception as e:
                print("Error:", e)

        # Phone (basic non-empty for now)
        while True:
            phone = input("Phone: ")
            if not phone.strip():
                print("Error: Phone number is required.")
            else:
                break

        # Username
        while True:
            username = input("Username: ")
            try:
                validate_username(username)
                break
            except Exception as e:
                print("Error:", e)

        # Password (simple non-empty)
        while True:
            password = input("Password: ")
            if not password.strip():
                print("Error: Password cannot be empty.")
            else:
                break

        # Role ID
        while True:
            role_id = input("Role ID: ")
            try:
                validate_role_id(role_id)
                role_id_int = int(role_id)
                break
            except Exception as e:
                print("Error:", e)

        # Build Staff object
        staff = Staff(
            full_name=full_name,
            email=email,
            phone=phone,
            username=username,
            password_hash=password,  # plain for now; can be hashed later
            role_id=role_id_int,
            status="Active",
        )

        # Save to DB
        if AdminManagementLib.admin_service.create_staff(staff):
            print("✅ Staff created successfully.")
        else:
            print("❌ Failed to create staff.")

    @staticmethod
    def list_staff():
        print("\n--- Staff List ---")
        staff_list = AdminManagementLib.admin_service.list_staff()
        if not staff_list:
            print("No staff found.")
            return
        for s in staff_list:
            print(s)

    @staticmethod
    def view_staff_by_id():
        """
        Fetch and display a single staff using staff_id
        """
        print("\n--- View Staff By ID ---")

        while True:
            staff_id = input("Enter Staff ID: ").strip()
            if not staff_id.isdigit():
                print("Error: Staff ID must be a number.")
                continue
            staff_id = int(staff_id)
            break

        staff = AdminManagementLib.admin_service.get_staff_by_id(staff_id)
        if staff is None:
            print(f"❌ No staff found with ID {staff_id}.")
        else:
            print("\nStaff Details:")
            print(staff)

    @staticmethod
    def deactivate_staff():
        print("\n--- Deactivate Staff ---")

        # Ask for Staff ID
        while True:
            staff_id = input("Enter Staff ID to deactivate: ")
            if not staff_id.isdigit():
                print("Error: Staff ID must be a number.")
                continue
            staff_id = int(staff_id)
            break

        staff = AdminManagementLib.admin_service.get_staff_by_id(staff_id)
        if staff is None:
            print(f"❌ No staff found with ID {staff_id}.")
            return

        print("\nCurrent Staff:")
        print(staff)

        confirm = input(f"Are you sure you want to deactivate Staff ID {staff_id}? (y/n): ").lower()
        if confirm != "y":
            print("Deactivation cancelled.")
            return

        if AdminManagementLib.admin_service.deactivate_staff(staff_id):
            print(f"✅ Staff ID {staff_id} deactivated successfully.")
        else:
            print(f"❌ Failed to deactivate Staff ID {staff_id}.")

    @staticmethod
    def delete_staff():
        print("\n--- Delete Staff ---")

        # Ask staff ID until valid
        while True:
            staff_id = input("Enter Staff ID to delete: ")

            if not staff_id.isdigit():
                print("Error: Staff ID must be a number.")
                continue

            staff_id = int(staff_id)
            break

        staff = AdminManagementLib.admin_service.get_staff_by_id(staff_id)
        if staff is None:
            print(f"❌ No staff found with ID {staff_id}.")
            return

        print("\nCurrent Staff:")
        print(staff)

        confirm = input(
            f"Are you sure you want to DELETE Staff ID {staff_id}? This cannot be undone. (y/n): "
        ).lower()

        if confirm != "y":
            print("Deletion cancelled.")
            return

        # Call DAO service
        if AdminManagementLib.admin_service.delete_staff(staff_id):
            print(f"✅ Staff ID {staff_id} deleted successfully.")
        else:
            print(f"❌ Failed to delete Staff ID {staff_id}.")

    @staticmethod
    def update_staff():
        print("\n--- Update Staff (Single Field) ---")

        # Staff ID
        while True:
            staff_id = input("Enter Staff ID to update: ").strip()
            if not staff_id.isdigit():
                print("Error: Staff ID must be a number.")
                continue
            staff_id = int(staff_id)
            break

        # Fetch current staff
        staff = AdminManagementLib.admin_service.get_staff_by_id(staff_id)
        if staff is None:
            print(f"❌ No staff found with ID {staff_id}.")
            return

        print("\nCurrent Staff:")
        print(staff)

        # Choose field to update
        print("""
Which field do you want to update?

1. Full Name
2. Email
3. Phone
4. Role ID
5. Status (Active/Inactive)
0. Cancel
        """)

        choice = input("Enter choice: ").strip()

        if choice == "0":
            print("Update cancelled.")
            return

        field_name = None
        new_value = None

        # 1. Full Name
        if choice == "1":
            while True:
                full_name = input("New Full Name: ")
                try:
                    validate_staff_name(full_name)
                    field_name = "full_name"
                    new_value = full_name
                    break
                except Exception as e:
                    print("Error:", e)

        # 2. Email
        elif choice == "2":
            while True:
                email = input("New Email: ")
                try:
                    validate_email(email)
                    field_name = "email"
                    new_value = email
                    break
                except Exception as e:
                    print("Error:", e)

        # 3. Phone
        elif choice == "3":
            while True:
                phone = input("New Phone: ")
                if not phone.strip():
                    print("Error: Phone cannot be empty.")
                    continue
                field_name = "phone"
                new_value = phone
                break

        # 4. Role ID
        elif choice == "4":
            while True:
                role_id = input("New Role ID: ")
                try:
                    validate_role_id(role_id)
                    field_name = "role_id"
                    new_value = int(role_id)
                    break
                except Exception as e:
                    print("Error:", e)

        # 5. Status
        elif choice == "5":
            while True:
                status = input("New Status (Active/Inactive): ").strip()
                if status not in ("Active", "Inactive"):
                    print("Error: Status must be 'Active' or 'Inactive'.")
                    continue
                field_name = "status"
                new_value = status
                break

        else:
            print("Invalid choice. Update cancelled.")
            return

        # Confirm update
        confirm = input(
            f"Are you sure you want to update Staff ID {staff_id} field '{field_name}'? (y/n): "
        ).lower()

        if confirm != "y":
            print("Update cancelled.")
            return

        # Call DAO
        if AdminManagementLib.admin_service.update_staff_field(staff_id, field_name, new_value):
            print("✅ Staff updated successfully.")
        else:
            print("❌ Failed to update staff. Check Staff ID.")

    @staticmethod
    def view_roles():
        print("\n--- Roles ---")
        roles = AdminManagementLib.admin_service.list_roles()
        if not roles:
            print("No roles found.")
            return
        for r in roles:
            print(f"ID: {r['role_id']}, Name: {r['role_name']}")

    @staticmethod
    def view_departments():
        print("\n--- Departments ---")
        depts = AdminManagementLib.admin_service.list_departments()
        if not depts:
            print("No departments found.")
            return
        for d in depts:
            print(
                f"ID: {d['department_id']}, Name: {d['department_name']}, "
                f"Status: {d['status']}, Desc: {d['description']}"
            )

    @staticmethod
    def view_audit_logs():
        print("\n--- Latest Audit Logs ---")
        logs = AdminManagementLib.admin_service.list_audit_logs()
        if not logs:
            print("No logs found.")
            return
        for log in logs:
            print(
                f"ID: {log['log_id']}, Staff: {log['staff_id']}, "
                f"Action: {log['action_type']}, Entity: {log['entity_name']}({log['entity_id']}), "
                f"Time: {log['action_timestamp']}"
            )
