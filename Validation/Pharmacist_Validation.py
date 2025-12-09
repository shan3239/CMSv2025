
# Validation/Pharmacist_Validation.py
from datetime import datetime, date
import re

class PharmacistValidation:

    # ---------- ADD MEDICINE ----------

    @staticmethod
    def validate_medicine_name(name: str) -> bool:
        if not name.strip():
            return False
        return bool(re.fullmatch(r"[A-Za-z\s.]+", name))

    @staticmethod
    def validate_category(category: str) -> bool:
        if not category.strip():
            return False
        allowed = {"antibiotic", "analgesic", "antipyretic", "vitamin", "antiseptic", "antifungal","chocolate"}
        return category.lower() in allowed

    @staticmethod
    def validate_form(form: str) -> bool:
        if not form.strip():
            return False
        allowed = {"tablet", "capsule", "syrup", "injection", "drops", "ointment"}
        return form.lower() in allowed

    @staticmethod
    def validate_strength(strength: str) -> bool:
        if not strength.strip():
            return False
        has_number = bool(re.search(r"\d", strength))
        has_unit = bool(re.search(r"(mg|ml|g|mcg|iu|%)", strength, re.I))
        return has_number and has_unit

    @staticmethod
    def validate_duplicate_medicine(name, form, strength, dao) -> bool:
        meds = dao.list_medicines_with_stock()
        for m in meds:
            if (m["medicine_name"].lower() == name.lower()
                and m["form"].lower() == form.lower()
                and m["strength"].lower() == strength.lower()):
                return False
        return True

    # ---------- ADD BATCH ----------

    @staticmethod
    def validate_medicine_id(mid: str, dao) -> bool:
        if not mid.isdigit():
            return False
        mid = int(mid)
        meds = dao.list_medicines_with_stock()
        return any(m["medicine_id"] == mid for m in meds)

    @staticmethod
    def validate_batch_number(batch: str, medicine_id: int, dao) -> bool:
        if not batch.strip():
            return False
        batches = dao.list_batches_for_medicine(medicine_id)
        return not any(b["batch_number"].lower() == batch.lower() for b in batches)

    @staticmethod
    def validate_expiry_date(expiry: str) -> bool:
        try:
            d = datetime.strptime(expiry, "%Y-%m-%d").date()
            return d > date.today()
        except:
            return False

    @staticmethod
    def validate_quantity(qty: str) -> bool:
        if not qty.isdigit():
            return False
        return int(qty) >= 0

    @staticmethod
    def validate_reorder_level(reorder: str) -> bool:
        if not reorder.strip():
            return True
        return reorder.isdigit() and int(reorder) >= 0

    # ---------- NEAR EXPIRY ----------

    @staticmethod
    def validate_days(days: str) -> bool:
        if not days.isdigit():
            return False
        days = int(days)
        return 1 <= days <= 365

    # ---------- DISPENSE ----------

    @staticmethod
    def validate_prescription_id(pid: str) -> bool:
        return pid.isdigit() and int(pid) > 0

    @staticmethod
    def validate_batch_choice(bid: str, batches) -> bool:
        if not bid.isdigit():
            return False
        bid = int(bid)
        return any(b["batch_id"] == bid for b in batches)

    @staticmethod
    def validate_dispense_quantity(qty: str, max_qty: int) -> bool:
        if not qty.isdigit():
            return False
        q = int(qty)
        return q > 0 and q <= max_qty

    # ---------- EXPIRE / RETURN ----------

    @staticmethod
    def validate_expire_batch(batch_id: str) -> bool:
        return batch_id.isdigit() and int(batch_id) > 0

    @staticmethod
    def validate_return_batch(batch_id: str) -> bool:
        return batch_id.isdigit() and int(batch_id) > 0