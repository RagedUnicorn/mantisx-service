from dataclasses import dataclass
from models.drill_settings import DrillSettings


@dataclass
class SessionExtras:
    hardware: str
    drill_settings: DrillSettings
    offsetRoll: float
    offsetPitch: float


def parse_session_extras(data):
    data["drill_settings"] = DrillSettings(**data["drill_settings"])
    return SessionExtras(**data)
