from dataclasses import dataclass
from typing import List, Optional
from models.shot_extras import ShotExtras
from models.shot_extras import parse_shot_extras


@dataclass
class Shot:
    pk: int
    score: str
    angle: str
    extras: ShotExtras
    session_pk: int
    problem: str
    pitch: List[float]
    yaw: List[float]
    bullseye: bool
    trigger_hold: str
    trigger_pull: str
    deleted: bool
    split: str
    hold_index: int
    pull_index: int
    shot_index: int
    absolute_pitch: List[float]
    absolute_roll: List[float]
    sample_rate: int
    holster_total_time: float
    grip_time: float
    holster_pull_time: float
    horizontal_time: float
    holster_target_time: float
    horizontal_to_shot_time: Optional[float] = None
    step_number: Optional[int] = None


def parse_shot(data):
    if not isinstance(data, dict):
        raise ValueError("Shot data must be a dictionary")
    
    # All fields except step_number and horizontal_to_shot_time are required
    required_fields = [
        'pk', 'score', 'angle', 'extras', 'session_pk', 'problem', 
        'pitch', 'yaw', 'bullseye', 'trigger_hold', 'trigger_pull', 
        'deleted', 'split', 'hold_index', 'pull_index', 'shot_index',
        'absolute_pitch', 'absolute_roll', 'sample_rate', 'holster_total_time',
        'grip_time', 'holster_pull_time', 'horizontal_time', 'holster_target_time'
    ]
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields for Shot: {missing_fields}")
    
    # Parse extras without mutating the original data
    extras = parse_shot_extras(data['extras'])
    
    # Build kwargs with only the fields we expect
    kwargs = {field: data[field] for field in required_fields if field != 'extras'}
    kwargs['extras'] = extras
    
    # Add optional fields if present
    if 'step_number' in data:
        kwargs['step_number'] = data['step_number']
    if 'horizontal_to_shot_time' in data:
        kwargs['horizontal_to_shot_time'] = data['horizontal_to_shot_time']
    
    return Shot(**kwargs)
