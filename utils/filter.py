from models.session import Session
from models.drill_type import DrillType


def filter_sessions_by_drill(sessions: list[Session], drill_type: DrillType) -> list[int]:
    """
    Filter sessions by drill type.
    
    Args:
        sessions: List of Session objects to filter
        drill_type: DrillType enum to match against session drill names
        
    Returns:
        List of session PKs that match the drill type
    """
    # Compare the string value of the enum with the session's drill_name string
    return [s.pk for s in sessions if s.drill_name == drill_type.value]
