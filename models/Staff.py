class Staff:
    def __init__(self, staff_id=None, full_name=None, email=None, phone=None, username=None,
                 password_hash=None, role_id=None, status="Active"):
        self.staff_id = staff_id
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.username = username
        self.password_hash = password_hash
        self.role_id = role_id
        self.status = status
