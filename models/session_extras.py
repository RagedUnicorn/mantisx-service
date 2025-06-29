from dataclasses import dataclass
from models.drill_settings import DrillSettings


@dataclass
class SessionExtras:
    hardware: str
    drill_settings: DrillSettings
    offsetRoll: float
    offsetPitch: float


def parse_session_extras(data):
    if not isinstance(data, dict):
        raise ValueError("SessionExtras data must be a dictionary")
    
    required_fields = ['hardware', 'drill_settings', 'offsetRoll', 'offsetPitch']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields for SessionExtras: {missing_fields}")
    
    # Parse drill_settings without mutating the original data
    if not isinstance(data['drill_settings'], dict):
        raise ValueError("drill_settings must be a dictionary")
    
    drill_settings = DrillSettings(**data['drill_settings'])
    
    # Only pass expected fields to avoid unexpected keyword arguments
    return SessionExtras(
        hardware=data['hardware'],
        drill_settings=drill_settings,
        offsetRoll=data['offsetRoll'],
        offsetPitch=data['offsetPitch']
    )
