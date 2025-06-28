import json

from dataclasses import dataclass
from models.session import Session
from models.session import parse_session


@dataclass
class SessionResponse:
    session: Session


def from_json(json_str: str) -> SessionResponse:
    data = json.loads(json_str)
    session = parse_session(data["session"])
    return SessionResponse(session=session)
