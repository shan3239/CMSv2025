from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class LabTechnicianDaoService(ABC):
    """
    Abstract DAO for Lab Technician use cases
    """

    # ---------- Lab Test Management ----------

    @abstractmethod
    def list_lab_tests(self) -> List[Dict]:
        """
        Return all lab tests.
        """
        pass

    @abstractmethod
    def add_lab_test(self, test_data: Dict) -> Optional[int]:
        """
        Insert a new lab test.
        Returns lab_test_id or None.
        """
        pass

    @abstractmethod
    def update_lab_test(self, lab_test_id: int, field_name: str, value) -> bool:
        """
        Update a single field of LAB_TEST.
        Allowed fields: test_name, category, description, normal_range, units, status.
        """
        pass

    # ---------- Lab Orders & Results ----------

    @abstractmethod
    def list_pending_lab_orders(self) -> List[Dict]:
        """
        List lab orders that are not completed yet.
        """
        pass

    @abstractmethod
    def get_lab_order_header(self, lab_order_id: int) -> Optional[Dict]:
        """
        Get a lab order with patient & doctor information.
        """
        pass

    @abstractmethod
    def get_lab_order_items_with_results(self, lab_order_id: int) -> List[Dict]:
        """
        Get lab order items joined with tests and any existing results.
        """
        pass

    @abstractmethod
    def insert_or_update_lab_result(
        self,
        lab_order_item_id: int,
        result_value: str,
        units: str,
        comments: str,
        technician_staff_id: int,
    ) -> bool:
        """
        Insert a new result or update existing result for a lab_order_item.
        """
        pass

    @abstractmethod
    def update_lab_order_status(self, lab_order_id: int, status: str) -> bool:
        """
        Update the status of a lab order (e.g., Pending, In Progress, Completed).
        """
        pass

    @abstractmethod
    def are_all_results_entered(self, lab_order_id: int) -> bool:
        """
        Check if every LAB_ORDER_ITEM for a given lab_order_id has a LAB_RESULT.
        """
        pass
