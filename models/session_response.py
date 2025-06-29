import json

from dataclasses import dataclass
from models.session import Session
from models.session import parse_session


@dataclass
class SessionResponse:
    session: Session


def from_json(json_str: str) -> SessionResponse:
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
    
    if not isinstance(data, dict):
        raise ValueError("JSON must be an object/dictionary")
    
    if "session" not in data:
        raise ValueError("Missing required field: session")
    
    try:
        session = parse_session(data["session"])
    except Exception as e:
        raise ValueError(f"Failed to parse session: {e}")
    
    return SessionResponse(session=session)
