from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class ReceptionistDaoService(ABC):
    """
    Abstract DAO for Receptionist use cases
    """

    # ---------- Patient Management ----------

    @abstractmethod
    def register_patient(self, patient_data: Dict) -> Optional[int]:
        """
        Insert a new patient record.
        Returns new patient_id or None on failure.
        """
        pass

    @abstractmethod
    def list_patients(self) -> List[Dict]:
        """
        Return a list of all patients.
        """
        pass

    @abstractmethod
    def get_patient_by_id(self, patient_id: int) -> Optional[Dict]:
        """
        Fetch single patient by ID.
        """
        pass

    # ---------- Appointment Management ----------

    @abstractmethod
    def list_doctors(self) -> List[Dict]:
        """
        Return list of doctors (id, name, specialization).
        """
        pass

    @abstractmethod
    def schedule_appointment(
        self,
        patient_id: int,
        doctor_id: int,
        scheduled_datetime: str,
        reason_for_visit: str,
        created_by_staff_id: int
    ) -> Optional[int]:
        """
        Create a new appointment.
        Returns appointment_id or None.
        """
        pass

    @abstractmethod
    def get_appointments_by_date(self, date_str: str) -> List[Dict]:
        """
        Return list of appointments on a given date.
        """
        pass

    # ---------- Billing ----------

    @abstractmethod
    def create_consultation_bill(self, appointment_id: int) -> Optional[int]:
        """
        Create a consultation bill for a completed appointment.
        Uses doctor's consultation_fee.
        Returns bill_id or None.
        """
        pass

    @abstractmethod
    def get_appointment_details(self, appointment_id: int) -> Optional[Dict]:
        """
        Fetch appointment with patient & doctor info.
        """
        pass
