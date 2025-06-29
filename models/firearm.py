from dataclasses import dataclass


@dataclass
class Firearm:
    make: str
    model: str
    caliber: str


def parse_firearm(data):
    if not isinstance(data, dict):
        raise ValueError("Firearm data must be a dictionary")
    
    required_fields = ['make', 'model', 'caliber']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields for Firearm: {missing_fields}")
    
    # Only pass expected fields to avoid unexpected keyword arguments
    return Firearm(
        make=data['make'],
        model=data['model'],
        caliber=data['caliber']
    )
