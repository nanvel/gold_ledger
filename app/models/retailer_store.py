from dataclasses import dataclass

from .user import User


@dataclass
class RetailerStore:
    id: int
    name: str
    admin_id: int
