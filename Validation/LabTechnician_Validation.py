# Validation/LabTechnician_Validation.py
from datetime import datetime
import re


class LabTechnicianValidation:

    # ---------- ADD LAB TEST ----------

    @staticmethod
    def validate_test_name(name: str) -> bool:
        # Only letters and spaces, Min 3 chars
        return bool(re.fullmatch(r"[A-Za-z ]{3,}", name))

    @staticmethod
    def validate_category(category: str) -> bool:
        # Only letters, Min 3 chars
        return bool(re.fullmatch(r"[A-Za-z ]{3,}", category))

    @staticmethod
    def validate_description(desc: str) -> bool:
        # Must not be empty, letters + numbers + spaces + comma + dot
        return bool(re.fullmatch(r"[A-Za-z0-9 ,.]{5,}", desc))

    @staticmethod
    def validate_normal_range(value: str) -> bool:
        # Example: 4.2-5.6 OR 70-110
        return bool(re.fullmatch(r"\d+(\.\d+)?\s*-\s*\d+(\.\d+)?", value))

    @staticmethod
    def validate_units(units: str) -> bool:
        allowed_units = {
        "mg/dl",
        "g/dl",
        "mmol/l",
        "iu/l",
        "cells/mm3",
        "percentage"
    }
        return units.lower() in allowed_units

    @staticmethod
    def validate_status(status: str) -> bool:
        return status.lower() in {"active", "inactive"}

    # ---------- UPDATE TEST ----------

    @staticmethod
    def validate_test_field_choice(choice: str) -> bool:
        return choice in {"0", "1", "2", "3", "4", "5", "6"}

    # ---------- RECORD RESULT ----------

    @staticmethod
    def validate_lab_order_id(oid: str) -> bool:
        return oid.isdigit() and int(oid) > 0

    @staticmethod
    def validate_result_value(value: str) -> bool:
        # Accept:
        # 234, 5.6, Positive, Negative, Normal
        return bool(re.fullmatch(r"[A-Za-z0-9.]+", value))

    @staticmethod
    def validate_units_optional(units: str) -> bool:
        if not units:
            return True
        return bool(re.fullmatch(r"[A-Za-z/%]+", units))

    @staticmethod
    def validate_comments(comments: str) -> bool:
        # Allow blank OR clean comments
        if not comments:
            return True
        return bool(re.fullmatch(r"[A-Za-z0-9 ,.]+", comments))