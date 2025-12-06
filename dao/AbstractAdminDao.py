from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from models.staff import Staff


class AdminDaoService(ABC):
    """
    Abstract methods for Admin use cases (Staff, Roles, Departments, Logs)
    """

    @abstractmethod
    def create_staff(self, staff: Staff) -> bool:
        """
        Insert a new staff record into the database.
        Returns True if exactly one row was inserted.
        """
        pass

    @abstractmethod
    def list_staff(self) -> List[Staff]:
        """
        Return a list of all staff as Staff objects.
        """
        pass

    @abstractmethod
    def get_staff_by_id(self, staff_id: int) -> Optional[Staff]:
        """
        Fetch a single Staff by staff_id.
        Returns Staff if found, else None.
        """
        pass

    @abstractmethod
    def deactivate_staff(self, staff_id: int) -> bool:
        """
        Set staff status to 'Inactive' for the given staff_id.
        Returns True if one row was updated.
        """
        pass

    @abstractmethod
    def delete_staff(self, staff_id: int) -> bool:
        """
        Hard delete a staff record from the database.
        Returns True if one row was deleted.
        """
        pass

    @abstractmethod
    def update_staff_field(self, staff_id: int, field_name: str, value) -> bool:
        """
        Update a single allowed field of a staff record.
        field_name must be one of: full_name, email, phone, role_id, status.
        Returns True if one row was updated.
        """
        pass

    @abstractmethod
    def list_roles(self) -> List[Dict]:
        """
        Return all roles as a list of dictionaries:
        { 'role_id': ..., 'role_name': ... }
        """
        pass

    @abstractmethod
    def list_audit_logs(self) -> List[Dict]:
        """
        Return recent audit logs as a list of dictionaries.
        """
        pass

    @abstractmethod
    def list_departments(self) -> List[Dict]:
        """
        Return all departments as a list of dictionaries.
        """
        pass

