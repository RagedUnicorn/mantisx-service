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
    horizontal_to_shot_time: float
    step_number: Optional[int] = None


def parse_shot(data):
    data["extras"] = parse_shot_extras(data["extras"])
    return Shot(**data)
