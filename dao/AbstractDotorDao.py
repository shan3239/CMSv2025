from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class DoctorDaoService(ABC):
    """
    Abstract methods for Doctor use cases
    """

    @abstractmethod
    def get_doctor_id_by_staff_id(self, staff_id: int) -> Optional[int]:
        pass

    @abstractmethod
    def get_appointments_for_doctor(self, doctor_id: int) -> List[Dict]:
        pass

    @abstractmethod
    def get_appointment_details(self, appointment_id: int) -> Optional[Dict]:
        pass

    @abstractmethod
    def insert_consultation_note(self, appointment_id: int, doctor_id: int,
                                 symptoms: str, observations: str,
                                 diagnosis: str, recommendations: str) -> bool:
        pass

    @abstractmethod
    def create_prescription(self, appointment_id: int, doctor_id: int) -> Optional[int]:
        pass

    @abstractmethod
    def add_prescription_item(self, prescription_id: int, medicine_id: int,
                              dosage: str, frequency: str,
                              duration: str, instructions: str) -> bool:
        pass

    @abstractmethod
    def list_medicines(self) -> List[Dict]:
        pass

    @abstractmethod
    def create_lab_order(self, appointment_id: int, patient_id: int,
                         doctor_id: int, notes: str) -> Optional[int]:
        pass

    @abstractmethod
    def add_lab_order_item(self, lab_order_id: int, lab_test_id: int,
                           notes: str) -> bool:
        pass

    @abstractmethod
    def list_lab_tests(self) -> List[Dict]:
        pass

    @abstractmethod
    def get_patient_medical_history(self, patient_id: int) -> Dict:
        pass

    @abstractmethod
    def insert_patient_vitals(self, appointment_id: int, staff_id: int,
                              bp: str, temp: float,
                              pulse: int, spo2: int,
                              rr: int) -> bool:
        pass

    @abstractmethod
    def get_lab_results_for_doctor(self, doctor_id: int) -> List[Dict]:
        pass

    @abstractmethod
    def update_diagnosis(self, consultation_id: int, new_diagnosis: str) -> bool:
        pass

    @abstractmethod
    def create_followup_appointment(self, old_appointment_id: int,
                                    new_datetime: str,
                                    reason: str) -> bool:
        pass
