import logging

from network import network_util
from models.user_data import UserData
from models.session_response import SessionResponse
from models.session_response import from_json
from utils.retry import retry_with_backoff


@retry_with_backoff(max_retries=3, backoff_factor=1.0)
def get_session(user_data: UserData, session_pk: int) -> SessionResponse:
    url = "https://train.mantisx.com/get-session"
    headers_with_csrf = network_util.prepare_csrf_headers()

    payload = {
        "user_pk": user_data.user_pk,
        "user_secret_key": user_data.user_secret_key,
        "session_pk": session_pk
    }

    logging.debug("Fetching session.py %s", session_pk)
    response = network_util.get_session().post(url, headers=headers_with_csrf, json=payload, timeout=30)

    if response.status_code == 200:
        logging.info("Session details for pk %s retrieved successfully", session_pk)
        try:
            return from_json(response.text)
        except Exception as e:
            error_msg = f"Failed to parse session response for pk {session_pk}: {e}"
            logging.error(error_msg)
            raise ValueError(error_msg) from e
    else:
        error_msg = f"Failed to retrieve session {session_pk}: HTTP {response.status_code}"
        logging.error(error_msg)
        raise RuntimeError(error_msg)
