import logging

from network import network_util
from models.user_data import UserData
from datetime import datetime, timedelta, timezone
from models.session_list_response import SessionListResponse
from models.session_list_response import from_json


def get_sessions_history(user_data: UserData, days_back: int = None, start_date: str = None, end_date: str = None) -> SessionListResponse:
    if days_back is not None:
        logging.info("Retrieving sessions history for user: %s, days back: %d", user_data.username, days_back)
    else:
        logging.info("Retrieving sessions history for user: %s, date range: %s to %s", user_data.username, start_date or "N/A", end_date or "today")

    url = "https://train.mantisx.com/session-history"

    headers_with_csrf = network_util.prepare_csrf_headers()

    # Calculate date range
    if days_back is not None:
        # Use existing days_back logic
        now = datetime.now(timezone.utc)
        start = now - timedelta(days=days_back)
        start_date_iso = start.isoformat(timespec="milliseconds").replace("+00:00", "Z")
        end_date_iso = now.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    else:
        # Use date range logic
        if start_date:
            # Parse start_date from DD/MM/YYYY format
            start_dt = datetime.strptime(start_date, '%d/%m/%Y').replace(tzinfo=timezone.utc)
            start_date_iso = start_dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")
        else:
            # This shouldn't happen due to validation in main.py, but just in case
            start_dt = datetime.now(timezone.utc) - timedelta(days=1)
            start_date_iso = start_dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")

        if end_date:
            # Parse end_date from DD/MM/YYYY format and set to end of day
            end_dt = datetime.strptime(end_date, '%d/%m/%Y').replace(hour=23, minute=59, second=59, microsecond=999000, tzinfo=timezone.utc)
            end_date_iso = end_dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")
        else:
            # Default to today (end of day)
            now = datetime.now(timezone.utc)
            end_dt = now.replace(hour=23, minute=59, second=59, microsecond=999000)
            end_date_iso = end_dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")

    payload = {
        "user_pk": user_data.user_pk,
        "user_secret_key": user_data.user_secret_key,
        "profiled_user_pk": str(user_data.user_pk),
        "start_date": start_date_iso,
        "end_date": end_date_iso,
        "type": "pistol",
        "highlights": False
    }

    response = network_util.get_session().post(url, headers=headers_with_csrf, json=payload, timeout=30)

    if response.status_code == 200:
        logging.info("Sessions history retrieved successfully!")
        return from_json(response.text)
    else:
        logging.error("Failed to retrieve sessions history with status code: %s", response.status_code)
        raise RuntimeError(f"Failed to retrieve sessions history: HTTP {response.status_code}")
