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

        name = input("Medicine Name: ").strip()
        if not PharmacistValidation.validate_medicine_name(name):
            print("❌ Invalid Medicine Name"); return

        category = input("Category (Antibiotic/Analgesic etc): ").strip()
        if not PharmacistValidation.validate_category(category):
            print("❌ Invalid Category"); return

        form = input("Form (Tablet/Capsule/etc): ").strip()
        if not PharmacistValidation.validate_form(form):
            print("❌ Invalid Form"); return

        strength = input("Strength (e.g., 500mg): ").strip()
        if not PharmacistValidation.validate_strength(strength):
            print("❌ Invalid Strength"); return

        if not PharmacistValidation.validate_duplicate_medicine(
            name, form, strength, PharmacistManagementLib.dao
        ):
            print("❌ Duplicate Medicine Exists"); return

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

        mid = input("Medicine ID: ").strip()
        if not PharmacistValidation.validate_medicine_id(mid, PharmacistManagementLib.dao):
            print("❌ Invalid Medicine ID"); return
        medicine_id = int(mid)

        batch = input("Batch Number: ").strip()
        if not PharmacistValidation.validate_batch_number(batch, medicine_id, PharmacistManagementLib.dao):
            print("❌ Batch number invalid or duplicate"); return

        expiry = input("Expiry Date (YYYY-MM-DD): ").strip()
        if not PharmacistValidation.validate_expiry_date(expiry):
            print("❌ Invalid Expiry Date"); return

        qty = input("Quantity on Hand: ").strip()
        if not PharmacistValidation.validate_quantity(qty):
            print("❌ Invalid Quantity"); return
        qty = int(qty)

        reorder = input("Reorder Level (optional): ").strip()
        if not PharmacistValidation.validate_reorder_level(reorder):
            print("❌ Invalid Reorder Level"); return
        reorder_level = int(reorder) if reorder.strip() else None

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
        days = input("Days (1–365): ").strip()
        if not PharmacistValidation.validate_days(days):
            print("❌ Invalid Days"); return

        batches = PharmacistManagementLib.dao.list_near_expiry_batches(int(days))
        if not batches:
            print("No near-expiry batches."); return

        for b in batches:
            print(f"{b['medicine_name']} | {b['batch_number']} | Exp {b['expiry_date']}")

    # ---------- Expired ----------

    @staticmethod
    def view_expired():
        print("\n--- Expired Medicines ---")
        batches = PharmacistManagementLib.dao.list_expired_batches()
        if not batches:
            print("No expired batches."); return

        for b in batches:
            print(f"{b['medicine_name']} | {b['batch_number']} | Exp {b['expiry_date']}")

    # ---------- Remove Expired ----------

    @staticmethod
    def remove_expired_batch():
        print("\n--- Remove / Mark Expired Batch ---")
        PharmacistManagementLib.view_expired()

        bid = input("Batch ID: ").strip()
        if not PharmacistValidation.validate_expire_batch(bid):
            print("❌ Invalid Batch ID"); return

        ok = PharmacistManagementLib.dao.mark_batch_expired(int(bid))
        print("✅ Marked expired" if ok else "❌ Failed")

    # ---------- Return to Supplier ----------

    @staticmethod
    def mark_return_to_supplier():
        print("\n--- Mark Batch as Return to Supplier ---")
        PharmacistManagementLib.view_expired()

        bid = input("Batch ID: ").strip()
        if not PharmacistValidation.validate_return_batch(bid):
            print("❌ Invalid Batch ID"); return

        ok = PharmacistManagementLib.dao.mark_batch_return_to_supplier(int(bid))
        print("✅ Returned to supplier" if ok else "❌ Failed")

    # ---------- Dispense ----------

    @staticmethod
    def dispense_medication(user):
        print("\n--- Dispense Medication ---")

        pid = input("Prescription ID: ").strip()
        if not PharmacistValidation.validate_prescription_id(pid):
            print("❌ Invalid Prescription ID"); return
        pid = int(pid)

        header = PharmacistManagementLib.dao.get_prescription_header(pid)
        if not header:
            print("❌ Prescription not found."); return

        items = PharmacistManagementLib.dao.get_prescription_items(pid)
        if not items:
            print("No items found."); return

        for item in items:
            print(f"{item['medicine_name']} | {item['dosage']} | {item['frequency']}")

            batches = PharmacistManagementLib.dao.get_available_batches_for_medicine(item["medicine_id"])
            if not batches:
                print("⚠ No stock."); continue

            for b in batches:
                print(f"Batch {b['batch_id']} | Qty {b['quantity_on_hand']}")

            if input("Dispense? (y): ").lower() != "y":
                continue

            bid = input("Batch ID: ").strip()
            if not PharmacistValidation.validate_batch_choice(bid, batches):
                print("❌ Invalid Batch"); continue
            bid = int(bid)

            max_qty = next(b["quantity_on_hand"] for b in batches if b["batch_id"] == bid)
            qty = input("Quantity: ").strip()
            if not PharmacistValidation.validate_dispense_quantity(qty, max_qty):
                print("❌ Invalid Quantity"); continue

            ok = PharmacistManagementLib.dao.dispense_medicine(
                item["prescription_item_id"], bid, int(qty), user.staff_id
            )
            print("✅ Dispensed" if ok else "❌ Failed")