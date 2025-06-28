import json

from dataclasses import dataclass
from typing import List
from models.session import Session


@dataclass
class SessionListResponse:
    success: bool
    sessions: List[Session]


def from_json(json_str: str) -> SessionListResponse:
    from models.session import parse_session

    data = json.loads(json_str)
    sessions = [parse_session(session) for session in data["sessions"]]
    return SessionListResponse(success=data["success"], sessions=sessions)
