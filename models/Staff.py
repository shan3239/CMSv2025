class Staff:
    """
    Staff model class representing STAFF table with encapsulation.
    All attributes are private with getters and setters.
    """

    def __init__(
        self,
        staff_id=None,
        full_name=None,
        email=None,
        phone=None,
        username=None,
        password_hash=None,
        role_id=None,
        status=None,
        role_name=None
    ):
        self.__staff_id = staff_id
        self.__full_name = full_name
        self.__email = email
        self.__phone = phone
        self.__username = username
        self.__password_hash = password_hash
        self.__role_id = role_id
        self.__status = status
        # joined from ROLE table (optional)
        self.__role_name = role_name

    # ------------- staff_id -------------
    @property
    def staff_id(self):
        return self.__staff_id

    @staff_id.setter
    def staff_id(self, value):
        self.__staff_id = value

    # ------------- full_name -------------
    @property
    def full_name(self):
        return self.__full_name

    @full_name.setter
    def full_name(self, value):
        self.__full_name = value

    # ------------- email -------------
    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    # ------------- phone -------------
    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = value

    # ------------- username -------------
    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    # ------------- password_hash -------------
    @property
    def password_hash(self):
        return self.__password_hash

    @password_hash.setter
    def password_hash(self, value):
        self.__password_hash = value

    # ------------- role_id -------------
    @property
    def role_id(self):
        return self.__role_id

    @role_id.setter
    def role_id(self, value):
        self.__role_id = value

    # ------------- status -------------
    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    # ------------- role_name (from ROLE table) -------------
    @property
    def role_name(self):
        return self.__role_name

    @role_name.setter
    def role_name(self, value):
        self.__role_name = value

    def __str__(self):
        return (
            f"ID: {self.__staff_id}, "
            f"Name: {self.__full_name}, "
            f"Username: {self.__username}, "
            f"Role: {self.__role_name}, "
            f"Status: {self.__status}"
        )

