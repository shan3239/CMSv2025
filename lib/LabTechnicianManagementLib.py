
from dao.LabTechnicianDaoImpl import LabTechnicianDaoImpl
from validation.LabTechnician_Validation import LabTechnicianValidation
from datetime import datetime


class LabTechnicianManagementLib:

    dao = LabTechnicianDaoImpl()

    # ---------- Lab Test Management ----------

    @staticmethod
    def list_lab_tests():
        print("\n--- Lab Tests ---")
        tests = LabTechnicianManagementLib.dao.list_lab_tests()
        if not tests:
            print("No lab tests found.")
            return

        for t in tests:
            print(
                f"ID: {t['lab_test_id']}, Name: {t['test_name']}, "
                f"Category: {t['category']}, Units: {t['units']}, "
                f"Range: {t['normal_range']}, Status: {t['status']}"
            )

    @staticmethod
    def add_lab_test():
        print("\n--- Add New Lab Test ---")

        while True:
            test_name = input("Test Name: ").strip()
            if LabTechnicianValidation.validate_test_name(test_name):
                break
            print("❌ Invalid test name (letters only, min 3 chars)")

        while True:
            category = input("Category (Blood / Urine / Imaging): ").strip()
            if LabTechnicianValidation.validate_category(category):
                break
            print("❌ Invalid category")

        while True:
            description = input("Description: ").strip()
            if LabTechnicianValidation.validate_description(description):
                break
            print("❌ Description cannot be empty")

        while True:
            normal_range = input("Normal Range (e.g., 4.5 - 6.2): ").strip()
            if LabTechnicianValidation.validate_normal_range(normal_range):
                break
            print("❌ Invalid format. Example: 4.5 - 6.2")

        while True:
            units = input("Units (mg/dL, g/dL): ").strip()
            if LabTechnicianValidation.validate_units(units):
                break
            print("❌ Invalid units")

        status = "Active"

        test_data = {
            "test_name": test_name,
            "category": category,
            "description": description,
            "normal_range": normal_range,
            "units": units,
            "status": status,
        }

        lab_test_id = LabTechnicianManagementLib.dao.add_lab_test(test_data)
        print(f"✅ Lab test added with ID: {lab_test_id}" if lab_test_id else "❌ Failed")

    @staticmethod
    def update_lab_test():
        print("\n--- Update Lab Test ---")
        LabTechnicianManagementLib.list_lab_tests()

        while True:
            tid = input("Enter Lab Test ID: ").strip()
            if tid.isdigit():
                lab_test_id = int(tid)
                break
            print("❌ ID must be number")

        print("""
1. Test Name
2. Category
3. Description
4. Normal Range
5. Units
6. Status
0. Cancel
        """)

        while True:
            choice = input("Choice: ").strip()
            if LabTechnicianValidation.validate_test_field_choice(choice):
                break
            print("❌ Invalid option")

        if choice == "0":
            return

        fields = {
            "1": "test_name",
            "2": "category",
            "3": "description",
            "4": "normal_range",
            "5": "units",
            "6": "status"
        }

        field = fields[choice]

        while True:
            value = input("Enter new value: ").strip()

            ok = True

            if field == "test_name":
                ok = LabTechnicianValidation.validate_test_name(value)
            elif field == "category":
                ok = LabTechnicianValidation.validate_category(value)
            elif field == "description":
                ok = LabTechnicianValidation.validate_description(value)
            elif field == "normal_range":
                ok = LabTechnicianValidation.validate_normal_range(value)
            elif field == "units":
                ok = LabTechnicianValidation.validate_units(value)
            elif field == "status":
                ok = LabTechnicianValidation.validate_status(value)

            if ok:
                break
            print("❌ Invalid value for field")

        result = LabTechnicianManagementLib.dao.update_lab_test(lab_test_id, field, value)
        print("✅ Updated" if result else "❌ Failed")

    # ---------- LAB RESULTS ----------

    @staticmethod
    def record_lab_results(technician_staff):
        print("\n--- Record Lab Results ---")
        LabTechnicianManagementLib.view_pending_lab_orders()

        while True:
            oid = input("Lab Order ID: ").strip()
            if LabTechnicianValidation.validate_lab_order_id(oid):
                lab_order_id = int(oid)
                break
            print("❌ Invalid order ID")

        header = LabTechnicianManagementLib.dao.get_lab_order_header(lab_order_id)
        if not header:
            print("❌ Lab Order not found")
            return

        items = LabTechnicianManagementLib.dao.get_lab_order_items_with_results(lab_order_id)

        for item in items:
            print(f"{item['test_name']} | {item['category']}")

            if input("Enter result? (y): ").lower() != "y":
                continue

            while True:
                result_value = input("Result Value: ").strip()
                if LabTechnicianValidation.validate_result_value(result_value):
                    break
                print("❌ Invalid result format")

            while True:
                units = input("Units (optional): ").strip()
                if LabTechnicianValidation.validate_units_optional(units):
                    break
                print("❌ Invalid units")

            while True:
                comments = input("Remarks (optional): ").strip()
                if LabTechnicianValidation.validate_comments(comments):
                    break
                print("❌ Invalid comments")

            ok = LabTechnicianManagementLib.dao.insert_or_update_lab_result(
                lab_order_item_id=item["lab_order_item_id"],
                result_value=result_value,
                units=units or item["result_units"] or "",
                comments=comments,
                technician_staff_id=technician_staff.staff_id,
            )

            print("✅ Saved" if ok else "❌ Failed")

        # Update status
        if LabTechnicianManagementLib.dao.are_all_results_entered(lab_order_id):
            LabTechnicianManagementLib.dao.update_lab_order_status(lab_order_id, "Completed")
            print("✅ Order Completed")
        else:
            LabTechnicianManagementLib.dao.update_lab_order_status(lab_order_id, "In Progress")
            print("⚠ Order still in progress")

    @staticmethod
    def view_pending_lab_orders():
        orders = LabTechnicianManagementLib.dao.list_pending_lab_orders()
        for o in orders:
            print(f"{o['lab_order_id']} | {o['patient_name']} | {o['status']}")