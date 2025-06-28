from dataclasses import dataclass


@dataclass
class ShotExtras:
    showScore: bool
    isHolster: bool
    iteration: int


def parse_shot_extras(data):
    return ShotExtras(**data)
