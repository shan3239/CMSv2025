from datetime import datetime
from dao.PharmacistDaoImpl import PharmacistDaoImpl


class PharmacistManagementLib:
    """
    Console logic for Pharmacist use cases:
    - View & update medicine inventory
    - Add medicines & batches
    - View low stock
    - View near expiry / expired
    - Remove / mark expired
    - Dispense medicine based on prescription
    """

    dao = PharmacistDaoImpl()

    # ---------- Inventory Management ----------

    @staticmethod
    def view_medicine_inventory():
        print("\n--- Medicine Inventory ---")
        meds = PharmacistManagementLib.dao.list_medicines_with_stock()
        if not meds:
            print("No medicines found.")
            return

        for m in meds:
            print(
                f"ID: {m['medicine_id']}, Name: {m['medicine_name']}, "
                f"Form: {m['form']}, Strength: {m['strength']}, "
                f"Status: {m['status']}, Total Stock: {m['total_stock']}"
            )

    @staticmethod
    def add_medicine():
        print("\n--- Add New Medicine ---")

        name = input("Medicine Name: ").strip()
        category = input("Category (e.g., Antibiotic, Analgesic): ").strip()
        form = input("Form (e.g., Tablet, Syrup, Injection): ").strip()
        strength = input("Strength (e.g., 500mg, 5mg/ml): ").strip()

        status = "Active"

        med_data = {
            "medicine_name": name,
            "category": category,
            "form": form,
            "strength": strength,
            "status": status,
        }

        med_id = PharmacistManagementLib.dao.add_medicine(med_data)
        if med_id:
            print(f"✅ Medicine added with ID: {med_id}")
        else:
            print("❌ Failed to add medicine.")

    @staticmethod
    def add_medicine_batch():
        print("\n--- Add Medicine Batch ---")
        PharmacistManagementLib.view_medicine_inventory()

        # Medicine ID
        while True:
            mid = input("Enter Medicine ID for this batch: ").strip()
            if not mid.isdigit():
                print("Error: Medicine ID must be a number.")
                continue
            medicine_id = int(mid)
            break

        batch_number = input("Batch Number: ").strip()

        # Expiry date
        while True:
            exp_str = input("Expiry Date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(exp_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Error: Invalid date format.")

        # Qty
        while True:
            qty_str = input("Quantity on Hand: ").strip()
            if not qty_str.isdigit():
                print("Error: Quantity must be a number.")
                continue
            quantity_on_hand = int(qty_str)
            break

        # Reorder level
        reorder_level = None
        rl = input("Reorder Level (optional): ").strip()
        if rl:
            if rl.isdigit():
                reorder_level = int(rl)
            else:
                print("Warning: Invalid reorder level, ignoring.")

        batch_data = {
            "medicine_id": medicine_id,
            "batch_number": batch_number,
            "expiry_date": exp_str,
            "quantity_on_hand": quantity_on_hand,
            "reorder_level": reorder_level,
            "status": "Active",
        }

        batch_id = PharmacistManagementLib.dao.add_medicine_batch(batch_data)
        if batch_id:
            print(f"✅ Batch added with ID: {batch_id}")
        else:
            print("❌ Failed to add batch.")

    @staticmethod
    def view_low_stock():
        print("\n--- Low Stock Medicines (By Batch) ---")
        batches = PharmacistManagementLib.dao.get_low_stock_batches()
        if not batches:
            print("No low-stock batches found.")
            return

        for b in batches:
            print(
                f"Batch ID: {b['batch_id']}, Medicine: {b['medicine_name']}, "
                f"Batch: {b['batch_number']}, Qty: {b['quantity_on_hand']}, "
                f"Reorder Level: {b['reorder_level']}, Expiry: {b['expiry_date']}"
            )

    # ---------- Expiry Management ----------

    @staticmethod
    def view_near_expiry():
        print("\n--- Near-Expiry Medicines ---")
        days_str = input("Enter number of days (e.g., 30): ").strip()
        if not days_str.isdigit():
            print("Error: Days must be a number.")
            return
        days = int(days_str)

        batches = PharmacistManagementLib.dao.list_near_expiry_batches(days)
        if not batches:
            print("No near-expiry batches found.")
            return

        for b in batches:
            print(
                f"Batch ID: {b['batch_id']}, Medicine: {b['medicine_name']}, "
                f"Batch: {b['batch_number']}, Expiry: {b['expiry_date']}, "
                f"Qty: {b['quantity_on_hand']}, Status: {b['status']}"
            )

    @staticmethod
    def view_expired():
        print("\n--- Expired Medicines ---")
        batches = PharmacistManagementLib.dao.list_expired_batches()
        if not batches:
            print("No expired batches found.")
            return

        for b in batches:
            print(
                f"Batch ID: {b['batch_id']}, Medicine: {b['medicine_name']}, "
                f"Batch: {b['batch_number']}, Expiry: {b['expiry_date']}, "
                f"Qty: {b['quantity_on_hand']}, Status: {b['status']}"
            )

    @staticmethod
    def remove_expired_batch():
        print("\n--- Remove / Mark Expired Batch ---")
        PharmacistManagementLib.view_expired()

        bid = input("Enter Batch ID to mark as Expired (set qty=0): ").strip()
        if not bid.isdigit():
            print("Error: Batch ID must be a number.")
            return

        batch_id = int(bid)
        if PharmacistManagementLib.dao.mark_batch_expired(batch_id):
            print(f"✅ Batch {batch_id} marked as Expired and removed from stock.")
        else:
            print("❌ Failed to mark batch expired.")

    @staticmethod
    def mark_return_to_supplier():
        print("\n--- Mark Batch as Return to Supplier ---")
        PharmacistManagementLib.view_expired()

        bid = input("Enter Batch ID to mark as ReturnToSupplier: ").strip()
        if not bid.isdigit():
            print("Error: Batch ID must be a number.")
            return

        batch_id = int(bid)
        if PharmacistManagementLib.dao.mark_batch_return_to_supplier(batch_id):
            print(f"✅ Batch {batch_id} marked as ReturnToSupplier.")
        else:
            print("❌ Failed to update batch status.")

    # ---------- Dispense Medicines ----------

    @staticmethod
    def dispense_medication(pharmacist_staff):
        """
        pharmacist_staff: Staff object (for dispensed_by_staff_id)
        """
        print("\n--- Dispense Medication ---")

        # Prescription ID
        while True:
            pid = input("Enter Prescription ID: ").strip()
            if not pid.isdigit():
                print("Error: Prescription ID must be a number.")
                continue
            prescription_id = int(pid)
            break

        # Fetch header
        header = PharmacistManagementLib.dao.get_prescription_header(prescription_id)
        if not header:
            print("No such prescription found.")
            return

        print(
            f"Prescription #{header['prescription_id']} for Patient: "
            f"{header['patient_name']} (ID: {header['patient_id']})"
        )

        # Fetch items
        items = PharmacistManagementLib.dao.get_prescription_items(prescription_id)
        if not items:
            print("No items found in this prescription.")
            return

        # For each item, dispense from selected batch
        for item in items:
            print("\n------------------------------")
            print(
                f"Item ID: {item['prescription_item_id']}, "
                f"Medicine: {item['medicine_name']} (ID: {item['medicine_id']}), "
                f"Dosage: {item['dosage']}, Freq: {item['frequency']}, "
                f"Duration: {item['duration']}"
            )

            # Show available batches for this medicine
            batches = PharmacistManagementLib.dao.get_available_batches_for_medicine(
                item["medicine_id"]
            )
            if not batches:
                print("⚠ No available stock for this medicine. Skipping.")
                continue

            print("Available Batches:")
            for b in batches:
                print(
                    f"Batch ID: {b['batch_id']}, Batch: {b['batch_number']}, "
                    f"Expiry: {b['expiry_date']}, Qty: {b['quantity_on_hand']}"
                )

            # Ask if we want to dispense this item
            choice = input(
                "Dispense this medicine? (y to dispense, any other key to skip): "
            ).strip().lower()
            if choice != "y":
                continue

            # Choose batch
            while True:
                bid = input("Enter Batch ID to dispense from: ").strip()
                if not bid.isdigit():
                    print("Error: Batch ID must be a number.")
                    continue
                batch_id = int(bid)
                if not any(b["batch_id"] == batch_id for b in batches):
                    print("Error: Batch ID not in available list.")
                    continue
                break

            # Quantity to dispense
            while True:
                qty_str = input("Quantity to dispense: ").strip()
                if not qty_str.isdigit():
                    print("Error: Quantity must be a number.")
                    continue
                qty = int(qty_str)
                if qty <= 0:
                    print("Error: Quantity must be > 0.")
                    continue
                break

            success = PharmacistManagementLib.dao.dispense_medicine(
                prescription_item_id=item["prescription_item_id"],
                batch_id=batch_id,
                quantity=qty,
                staff_id=pharmacist_staff.staff_id,
            )

            if success:
                print("✅ Dispensed successfully.")
            else:
                print("❌ Failed to dispense this item.")
