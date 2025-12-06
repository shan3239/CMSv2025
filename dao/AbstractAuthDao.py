from abc import ABC, abstractmethod
from typing import Optional
from models.staff import Staff

class AuthDaoService(ABC):
    """
    Authentication related DAO methods
    """

    @abstractmethod
    def authenticate(self, username: str, password: str) -> Optional[Staff]:
        """
        Validate username & password, return Staff object if valid, else None
        """
        pass
