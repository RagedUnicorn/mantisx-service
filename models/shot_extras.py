from dataclasses import dataclass


@dataclass
class ShotExtras:
    showScore: bool
    isHolster: bool
    iteration: int


def parse_shot_extras(data):
    if not isinstance(data, dict):
        raise ValueError("ShotExtras data must be a dictionary")
    
    required_fields = ['showScore', 'isHolster', 'iteration']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields for ShotExtras: {missing_fields}")
    
    # Only pass expected fields to avoid unexpected keyword arguments
    return ShotExtras(
        showScore=data['showScore'],
        isHolster=data['isHolster'],
        iteration=data['iteration']
    )
