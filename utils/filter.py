from models.session import Session
from models.drill_type import DrillType


def filter_sessions_by_drill(sessions: list[Session], drill_name: DrillType) -> list[int]:
    return [s.pk for s in sessions if s.drill_name == drill_name]
