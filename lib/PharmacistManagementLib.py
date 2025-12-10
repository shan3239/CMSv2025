
from datetime import datetime
from dao.PharmacistDaoImpl import PharmacistDaoImpl
from validation.Pharmacist_Validation import PharmacistValidation


class PharmacistManagementLib:

    dao = PharmacistDaoImpl()

    # ---------- Inventory ----------

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

    # ---------- Add Medicine ----------

    @staticmethod
    def add_medicine():
        print("\n--- Add New Medicine ---")

        while True:
            name = input("Medicine Name: ").strip()
            if PharmacistValidation.validate_medicine_name(name):
                break
            print("❌ Invalid Medicine Name")

        while True:
            category = input("Category (Antibiotic/Analgesic etc): ").strip()
            if PharmacistValidation.validate_category(category):
                break
            print("❌ Invalid Category")

        while True:
            form = input("Form (Tablet/Capsule/etc): ").strip()
            if PharmacistValidation.validate_form(form):
                break
            print("❌ Invalid Form")

        while True:
            strength = input("Strength (e.g., 500mg): ").strip()
            if PharmacistValidation.validate_strength(strength):
                break
            print("❌ Invalid Strength")

        while True:
            if PharmacistValidation.validate_duplicate_medicine(
                name, form, strength, PharmacistManagementLib.dao
            ):
                break
            print("❌ Duplicate Medicine Exists")
            strength = input("Re-enter Strength (or change Name/Form): ").strip()

        med_data = {
            "medicine_name": name,
            "category": category,
            "form": form,
            "strength": strength,
            "status": "Active",
        }

        med_id = PharmacistManagementLib.dao.add_medicine(med_data)
        print(f"✅ Medicine added with ID: {med_id}" if med_id else "❌ Failed to add medicine.")

    # ---------- Add Batch ----------

    @staticmethod
    def add_medicine_batch():
        print("\n--- Add Medicine Batch ---")
        PharmacistManagementLib.view_medicine_inventory()

        while True:
            mid = input("Medicine ID: ").strip()
            if PharmacistValidation.validate_medicine_id(mid, PharmacistManagementLib.dao):
                medicine_id = int(mid)
                break
            print("❌ Invalid Medicine ID")

        while True:
            batch = input("Batch Number: ").strip()
            if PharmacistValidation.validate_batch_number(batch, medicine_id, PharmacistManagementLib.dao):
                break
            print("❌ Batch number invalid or duplicate")

        while True:
            expiry = input("Expiry Date (YYYY-MM-DD): ").strip()
            if PharmacistValidation.validate_expiry_date(expiry):
                break
            print("❌ Invalid Expiry Date")

        while True:
            qty = input("Add Quantity: ").strip()
            if PharmacistValidation.validate_quantity(qty):
                qty = int(qty)
                break
            print("❌ Invalid Quantity")

        while True:
            reorder = input("Reorder Level (optional): ").strip()
            if PharmacistValidation.validate_reorder_level(reorder):
                reorder_level = int(reorder) if reorder.strip() else None
                break
            print("❌ Invalid Reorder Level")

        batch_data = {
            "medicine_id": medicine_id,
            "batch_number": batch,
            "expiry_date": expiry,
            "quantity_on_hand": qty,
            "reorder_level": reorder_level,
            "status": "Active",
        }

        bid = PharmacistManagementLib.dao.add_medicine_batch(batch_data)
        print(f"✅ Batch added with ID: {bid}" if bid else "❌ Failed to add batch.")

    # ---------- Low Stock ----------

    @staticmethod
    def view_low_stock():
        print("\n--- Low Stock Medicines (By Batch) ---")
        batches = PharmacistManagementLib.dao.get_low_stock_batches()
        if not batches:
            print("No low-stock batches found.")
            return
        for b in batches:
            print(f"{b['medicine_name']} | {b['batch_number']} | Qty {b['quantity_on_hand']}")

    # ---------- Near Expiry ----------

    @staticmethod
    def view_near_expiry():
        print("\n--- Near-Expiry Medicines ---")
        while True:
            days = input("Days (1-any days): ").strip()
            if PharmacistValidation.validate_days(days):
                days = int(days)
                break
            print("❌ Invalid Days")

        batches = PharmacistManagementLib.dao.list_near_expiry_batches(days)
        if not batches:
            print("No near-expiry batches.")
            return

        for b in batches:
            print(f"{b['medicine_name']} | {b['batch_number']} | Exp {b['expiry_date']}")

    # ---------- Expired ----------

    @staticmethod
    def view_expired():
        print("\n--- Expired Medicines ---")
        batches = PharmacistManagementLib.dao.list_expired_batches()
        if not batches:
            print("No expired batches.")
            return

        for b in batches:
            print(f"{b['medicine_name']} | {b['batch_number']} | Exp {b['expiry_date']}")

    # ---------- Remove Expired ----------

    @staticmethod
    def remove_expired_batch():
        print("\n--- Remove / Mark Expired Batch ---")
        PharmacistManagementLib.view_expired()

        while True:
            bid = input("Batch ID: ").strip()
            if PharmacistValidation.validate_expire_batch(bid):
                bid = int(bid)
                break
            print("❌ Invalid Batch ID")

        ok = PharmacistManagementLib.dao.mark_batch_expired(bid)
        print("✅ Marked expired" if ok else "❌ Failed")

    # ---------- Return to Supplier ----------

    @staticmethod
    def mark_return_to_supplier():
        print("\n--- Mark Batch as Return to Supplier ---")
        PharmacistManagementLib.view_expired()

        while True:
            bid = input("Batch ID: ").strip()
            if PharmacistValidation.validate_return_batch(bid):
                bid = int(bid)
                break
            print("❌ Invalid Batch ID")

        ok = PharmacistManagementLib.dao.mark_batch_return_to_supplier(bid)
        print("✅ Returned to supplier" if ok else "❌ Failed")

    # ---------- Dispense ----------

    @staticmethod
    def dispense_medication(user):
        print("\n--- Dispense Medication ---")

        while True:
            pid = input("Prescription ID: ").strip()
            if PharmacistValidation.validate_prescription_id(pid):
                pid = int(pid)
                break
            print("❌ Invalid Prescription ID")

        header = PharmacistManagementLib.dao.get_prescription_header(pid)
        if not header:
            print("❌ Prescription not found.")
            return

        items = PharmacistManagementLib.dao.get_prescription_items(pid)
        if not items:
            print("No items found.")
            return

        for item in items:
            print(f"{item['medicine_name']} | {item['dosage']} | {item['frequency']}")

            batches = PharmacistManagementLib.dao.get_available_batches_for_medicine(item["medicine_id"])
            if not batches:
                print("⚠ No stock.")
                continue

            for b in batches:
                print(f"Batch {b['batch_id']} | Qty {b['quantity_on_hand']}")

            if input("Dispense? (y): ").lower() != "y":
                continue

            while True:
                bid = input("Batch ID: ").strip()
                if PharmacistValidation.validate_batch_choice(bid, batches):
                    bid = int(bid)
                    break
                print("❌ Invalid Batch")

            max_qty = next(b["quantity_on_hand"] for b in batches if b["batch_id"] == bid)

            while True:
                qty = input("Quantity: ").strip()
                if PharmacistValidation.validate_dispense_quantity(qty, max_qty):
                    qty = int(qty)
                    break
                print("❌ Invalid Quantity")

            ok = PharmacistManagementLib.dao.dispense_medicine(
                item["prescription_item_id"], bid, qty, user.staff_id
            )
            print("✅ Dispensed" if ok else "❌ Failed")