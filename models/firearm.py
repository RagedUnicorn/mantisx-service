from dataclasses import dataclass


@dataclass
class Firearm:
    make: str
    model: str
    caliber: str


def parse_firearm(data):
    return Firearm(**data)
