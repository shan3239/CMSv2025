from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class PharmacistDaoService(ABC):
    """
    Abstract DAO for Pharmacist use cases
    """

    # ---------- Medicine & Inventory ----------

    @abstractmethod
    def list_medicines_with_stock(self) -> List[Dict]:
        """
        Return all medicines with total quantity_on_hand.
        """
        pass

    @abstractmethod
    def add_medicine(self, med_data: Dict) -> Optional[int]:
        """
        Insert new medicine row.
        Returns medicine_id or None.
        """
        pass

    @abstractmethod
    def add_medicine_batch(self, batch_data: Dict) -> Optional[int]:
        """
        Insert new batch for a medicine.
        Returns batch_id or None.
        """
        pass

    @abstractmethod
    def list_batches_for_medicine(self, medicine_id: int) -> List[Dict]:
        """
        List all batches for a given medicine.
        """
        pass

    @abstractmethod
    def update_batch_quantity(self, batch_id: int, new_qty: int) -> bool:
        """
        Update quantity_on_hand for a batch.
        """
        pass

    @abstractmethod
    def get_low_stock_batches(self) -> List[Dict]:
        """
        Batches where quantity_on_hand <= reorder_level and status='Active'.
        """
        pass

    # ---------- Expiry Management ----------

    @abstractmethod
    def list_near_expiry_batches(self, days: int) -> List[Dict]:
        """
        Batches expiring within next 'days' days.
        """
        pass

    @abstractmethod
    def list_expired_batches(self) -> List[Dict]:
        """
        Batches whose expiry_date < CURDATE() and status='Active'.
        """
        pass

    @abstractmethod
    def mark_batch_expired(self, batch_id: int) -> bool:
        """
        Mark batch as Expired and set quantity_on_hand = 0.
        """
        pass

    @abstractmethod
    def mark_batch_return_to_supplier(self, batch_id: int) -> bool:
        """
        Mark batch as ReturnToSupplier (optional workflow).
        """
        pass

    # ---------- Prescription & Dispensing ----------

    @abstractmethod
    def get_prescription_header(self, prescription_id: int) -> Optional[Dict]:
        """
        Fetch prescription with patient & doctor info.
        """
        pass

    @abstractmethod
    def get_prescription_items(self, prescription_id: int) -> List[Dict]:
        """
        Fetch prescription items with medicine name.
        """
        pass

    @abstractmethod
    def get_available_batches_for_medicine(self, medicine_id: int) -> List[Dict]:
        """
        Active batches with quantity_on_hand > 0 and not expired.
        """
        pass

    @abstractmethod
    def dispense_medicine(
        self,
        prescription_item_id: int,
        batch_id: int,
        quantity: int,
        staff_id: int,
    ) -> bool:
        """
        Insert into DISPENSED_MEDICINE and reduce batch quantity.
        """
        pass
