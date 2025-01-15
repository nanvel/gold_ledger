from dataclasses import dataclass

from .user_role import UserRole


@dataclass(frozen=True)
class User:
    id: int
    username: str
    password_hash: str
    role: UserRole
    token_version: int
