from dao.LabTechnicianDaoImpl import LabTechnicianDaoImpl


class LabTechnicianManagementLib:
    """
    Console logic for Lab Technician use cases:
    - Manage Lab Tests
    - View Pending Lab Orders
    - Record Lab Test Results
    """

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
        test_name = input("Test Name: ").strip()
        category = input("Category (e.g., Blood, Imaging, Urine): ").strip()
        description = input("Description: ").strip()
        normal_range = input("Normal Range (e.g., 4.0 - 5.5): ").strip()
        units = input("Units (e.g., mg/dL, g/dL): ").strip()
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
        if lab_test_id:
            print(f"✅ Lab test added with ID: {lab_test_id}")
        else:
            print("❌ Failed to add lab test.")

    @staticmethod
    def update_lab_test():
        print("\n--- Update Lab Test (Single Field) ---")
        LabTechnicianManagementLib.list_lab_tests()

        # Lab Test ID
        while True:
            tid = input("Enter Lab Test ID to update: ").strip()
            if not tid.isdigit():
                print("Error: ID must be a number.")
                continue
            lab_test_id = int(tid)
            break

        print("""
Which field do you want to update?

1. Test Name
2. Category
3. Description
4. Normal Range
5. Units
6. Status
0. Cancel
        """)

        choice = input("Enter choice: ").strip()

        field_name = None
        new_value = None

        if choice == "0":
            print("Update cancelled.")
            return
        elif choice == "1":
            field_name = "test_name"
            new_value = input("New Test Name: ").strip()
        elif choice == "2":
            field_name = "category"
            new_value = input("New Category: ").strip()
        elif choice == "3":
            field_name = "description"
            new_value = input("New Description: ").strip()
        elif choice == "4":
            field_name = "normal_range"
            new_value = input("New Normal Range: ").strip()
        elif choice == "5":
            field_name = "units"
            new_value = input("New Units: ").strip()
        elif choice == "6":
            field_name = "status"
            new_value = input("New Status (Active/Inactive): ").strip()
        else:
            print("Invalid choice.")
            return

        if not new_value:
            print("Error: New value cannot be empty.")
            return

        if LabTechnicianManagementLib.dao.update_lab_test(lab_test_id, field_name, new_value):
            print("✅ Lab test updated successfully.")
        else:
            print("❌ Failed to update lab test.")

    # ---------- Lab Orders & Results ----------

    @staticmethod
    def view_pending_lab_orders():
        print("\n--- Pending Lab Orders ---")
        orders = LabTechnicianManagementLib.dao.list_pending_lab_orders()
        if not orders:
            print("No pending lab orders found.")
            return

        for o in orders:
            print(
                f"Order ID: {o['lab_order_id']}, Date: {o['ordered_at']}, "
                f"Status: {o['status']}, Patient: {o['patient_name']} (ID: {o['patient_id']}), "
                f"Doctor: {o['doctor_name']}, Notes: {o['notes']}"
            )

    @staticmethod
    def record_lab_results(technician_staff):
        print("\n--- Record Lab Test Results ---")
        LabTechnicianManagementLib.view_pending_lab_orders()

        # Lab Order ID
        while True:
            oid = input("Enter Lab Order ID to record results for: ").strip()
            if not oid.isdigit():
                print("Error: Lab Order ID must be numeric.")
                continue
            lab_order_id = int(oid)
            break

        header = LabTechnicianManagementLib.dao.get_lab_order_header(lab_order_id)
        if not header:
            print("❌ Lab Order not found.")
            return

        print(
            f"\nRecording results for Lab Order #{header['lab_order_id']} "
            f"Patient: {header['patient_name']} (ID: {header['patient_id']}), "
            f"Doctor: {header['doctor_name']}"
        )

        items = LabTechnicianManagementLib.dao.get_lab_order_items_with_results(lab_order_id)
        if not items:
            print("No lab order items found.")
            return

        for item in items:
            print("\n-----------------------------")
            print(
                f"Item ID: {item['lab_order_item_id']}, Test: {item['test_name']} "
                f"(Category: {item['category']})"
            )
            print(f"Item Notes: {item['item_notes']}")
            if item["result_id"]:
                print(
                    f"Existing Result: {item['result_value']} {item['result_units']} "
                    f"({item['result_date']}) Comments: {item['comments']}"
                )

            choice = input("Enter/Update result for this test? (y to continue, anything else to skip): ").strip().lower()
            if choice != "y":
                continue

            result_value = input("Result Value: ").strip()
            units = input("Units (leave blank to use default test units, if known): ").strip()
            if not units:
                units = item["result_units"] if item["result_units"] else ""

            comments = input("Comments/Remarks (optional): ").strip()

            success = LabTechnicianManagementLib.dao.insert_or_update_lab_result(
                lab_order_item_id=item["lab_order_item_id"],
                result_value=result_value,
                units=units,
                comments=comments,
                technician_staff_id=technician_staff.staff_id,
            )

            if success:
                print("✅ Result saved.")
            else:
                print("❌ Failed to save result.")

        # After all items processed, check if order can be marked complete
        if LabTechnicianManagementLib.dao.are_all_results_entered(lab_order_id):
            updated = LabTechnicianManagementLib.dao.update_lab_order_status(
                lab_order_id, "Completed"
            )
            if updated:
                print(f"\n✅ All results entered. Lab Order #{lab_order_id} marked as Completed.")
            else:
                print("\n⚠ All results entered, but failed to update order status.")
        else:
            # Optionally mark as In Progress
            LabTechnicianManagementLib.dao.update_lab_order_status(lab_order_id, "In Progress")
            print("\nSome results are still missing. Order marked as In Progress.")
