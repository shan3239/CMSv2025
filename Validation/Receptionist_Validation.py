
# Validation/Receptionist_Validation.py
from datetime import datetime
import re


class ReceptionistValidation:

    # ---------- PATIENT REGISTRATION ----------

    @staticmethod
    def validate_full_name(name: str) -> bool:
        return bool(re.fullmatch(r"[A-Za-z\s.]{3,}", name))

    @staticmethod
    def validate_dob(dob: str) -> bool:
        if not dob:
            return True
        try:
            d = datetime.strptime(dob, "%Y-%m-%d")
            return d <= datetime.now()
        except:
            return False

    @staticmethod
    def validate_gender(gender: str) -> bool:
        if not gender:
            return True
        return gender.upper() in {"M", "F", "O"}

    @staticmethod
    def validate_phone(phone: str) -> bool:
        return bool(re.fullmatch(r"\d{10}", phone))

    @staticmethod
    def validate_email(email: str) -> bool:
        if not email:
            return True
        return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email))

    @staticmethod
    def validate_blood_group(bg: str) -> bool:
        if not bg:
            return True
        return bool(re.fullmatch(r"(A|B|AB|O)[+-]", bg.upper()))

    @staticmethod
    def validate_height(h: str) -> bool:
        if not h:
            return True
        try:
            return float(h) > 0
        except:
            return False

    @staticmethod
    def validate_weight(w: str) -> bool:
        if not w:
            return True
        try:
            return float(w) > 0
        except:
            return False

    @staticmethod
    def validate_membership(ms: str) -> bool:
        if not ms:
            return True
        return ms.lower() in {"regular", "premium"}

    # ---------- APPOINTMENT ----------

    @staticmethod
    def validate_patient_id(pid: str, dao) -> bool:
        if not pid.isdigit():
            return False
        return dao.get_patient_by_id(int(pid)) is not None

    @staticmethod
    def validate_doctor_id(did: str, doctors) -> bool:
        if not did.isdigit():
            return False
        did = int(did)
        return any(d["doctor_id"] == did for d in doctors)

    @staticmethod
    def validate_datetime(dt: str) -> bool:
        try:
            d = datetime.strptime(dt, "%Y-%m-%d %H:%M")
            return d >= datetime.now()
        except:
            return False
    @staticmethod
    def validate_reason(reason: str) -> bool:
        if not reason.strip():
            return False
        return bool(re.fullmatch(r"[A-Za-z\s.]+", reason))


    # ---------- VIEW APPOINTMENTS ----------

    @staticmethod
    def validate_date(date_str: str) -> bool:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except:
            return False

    # ---------- BILLING ----------

    @staticmethod
    def validate_appointment_id(appt_id: str) -> bool:
        return appt_id.isdigit() and int(appt_id) > 0