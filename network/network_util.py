import logging
from typing import Dict
import requests

_base_headers: Dict[str, str] = {
    "Authority": "train.mantisx.com",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9,de;q=0.8",
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://train.mantisx.com",
    "Referer": "https://train.mantisx.com/login/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

_session: requests.Session = None


def set_session(session: requests.Session):
    global _session
    _session = session


def get_session() -> requests.Session:
    if not _session:
        raise RuntimeError("Session not initialized. Call set_session(session) first.")
    return _session


def prepare_csrf_headers() -> Dict[str, str]:
    if not _session:
        raise RuntimeError("Session not initialized. Call set_session(session) first.")

    csrf_token = _session.cookies.get("csrftoken")
    if not csrf_token:
        logging.error("Missing CSRF token in session cookies.")
        raise RuntimeError("CSRF token not found in cookies. Cannot proceed.")

    return {
        **_base_headers,
        "X-CSRFToken": csrf_token,
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://train.mantisx.com/"
    }


def get_base_headers() -> Dict[str, str]:
    return _base_headers.copy()
