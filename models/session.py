from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from models.firearm import Firearm
from models.session_extras import SessionExtras
from models.shot import Shot
from models.session_extras import parse_session_extras
from models.firearm import parse_firearm
from models.shot import parse_shot


@dataclass
class Session:
    pk: int
    date: datetime
    user_pk: int
    username: str
    time_stamp: float
    right_handed: bool
    right_handed_display: str
    fire_type: int
    fire_type_display: str
    gun_type: int
    gun_type_display: str
    average_score: float
    stamp: str
    drill_id: int
    drill_name: str
    score_bars: int
    time_bars: int
    time_display: str
    deleted: bool
    shot_count: int
    notes: str
    manual_score: int
    course_number: int
    extras: SessionExtras
    comments: List[str]
    firearm: Firearm
    gun_display: str
    shots: List[Shot] = field(default_factory=list)


def parse_session(data):
    def get(key, default=None):
        return data[key] if key in data and data[key] is not None else default

    # Required date parsing
    date_str = get("date", "1970-01-01T00:00:00+00:00").replace("Z", "+00:00")
    data["date"] = datetime.fromisoformat(date_str)

    # Nested objects
    data["extras"] = parse_session_extras(get("extras", {
        "hardware": "",
        "drill_settings": { "repeat_count": 0 },
        "offsetRoll": 0.0,
        "offsetPitch": 0.0
    }))

    data["firearm"] = parse_firearm(get("firearm", {
        "make": "",
        "model": "",
        "caliber": ""
    }))

    data["shots"] = [parse_shot(shot) for shot in get("shots", [])]
    data["comments"] = get("comments", [])

    # Required scalars (fill all with defaults if missing)
    return Session(
        pk=get("pk", 0),
        date=data["date"],
        user_pk=get("user_pk", 0),
        username=get("username", ""),
        time_stamp=get("time_stamp", 0.0),
        right_handed=get("right_handed", True),
        right_handed_display=get("right_handed_display", "right"),
        fire_type=get("fire_type", 0),
        fire_type_display=get("fire_type_display", ""),
        gun_type=get("gun_type", 0),
        gun_type_display=get("gun_type_display", ""),
        average_score=get("average_score", 0.0),
        stamp=get("stamp", ""),
        drill_id=get("drill_id", 0),
        drill_name=get("drill_name", ""),
        score_bars=get("score_bars", 0),
        time_bars=get("time_bars", 0),
        time_display=get("time_display", ""),
        deleted=get("deleted", False),
        shot_count=get("shot_count", 0),
        notes=get("notes", ""),
        manual_score=get("manual_score", 0),
        course_number=get("course_number", -1),
        extras=data["extras"],
        comments=data["comments"],
        firearm=data["firearm"],
        gun_display=get("gun_display", ""),
        shots=data["shots"]
    )
