from dataclasses import dataclass, field


@dataclass
class Credentials:
    username: str
    password: str = field(repr=False)

