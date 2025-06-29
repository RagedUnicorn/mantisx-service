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

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
    
    if not isinstance(data, dict):
        raise ValueError("JSON must be an object/dictionary")
    
    if "success" not in data:
        raise ValueError("Missing required field: success")
    
    if "sessions" not in data:
        raise ValueError("Missing required field: sessions")
    
    if not isinstance(data["sessions"], list):
        raise ValueError("sessions must be an array")
    
    sessions = []
    for i, session_data in enumerate(data["sessions"]):
        try:
            sessions.append(parse_session(session_data))
        except Exception as e:
            raise ValueError(f"Failed to parse session at index {i}: {e}")
    
    return SessionListResponse(success=bool(data["success"]), sessions=sessions)
