from dataclasses import dataclass


@dataclass
class UserData:
    user_pk: int
    username: str
    email: str
    user_secret_key: str
