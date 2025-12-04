class AdminValidation:

    @staticmethod
    def validate_staff_data(staff):
        if not staff.full_name or len(staff.full_name.strip()) == 0:
            return False, "Full name is required."

        if not staff.username or len(staff.username.strip()) == 0:
            return False, "Username cannot be empty."

        if not staff.role_id:
            return False, "Role ID cannot be empty."

        return True, "Valid"
