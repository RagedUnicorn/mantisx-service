import logging

from pathlib import Path
from models.user_data import UserData
from models.credentials import Credentials
import network.network_util as network_util
from utils.retry import retry_with_backoff


def load_credentials() -> Credentials:
    """
    Loads credentials from a properties file in the user's home directory.
    The file can be named mantisx, mantisx.txt, mantis, or mantis.txt.
    """
    home_dir = Path.home()
    possible_files = ["mantisx", "mantisx.txt", "mantis", "mantis.txt"]
    credentials_file = None

    for file_name in possible_files:
        file_path = home_dir / file_name
        if file_path.is_file():
            credentials_file = file_path
            break

    if not credentials_file:
        error_msg = f"No credentials file found in the home directory. Expected one of: {possible_files}"
        logging.error(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        with open(credentials_file, 'r') as f:
            properties = dict(line.strip().split('=', 1) for line in f if '=' in line)
            return Credentials(
                username=properties['username'],
                password=properties['password']
            )
    except Exception as e:
        logging.error("Failed to parse the credentials file: %s", e)
        raise ValueError(f"Failed to parse the credentials file: {e}") from e


@retry_with_backoff(max_retries=3, backoff_factor=1.0)
def login() -> UserData:
    credentials = load_credentials()
    login_payload = {
        "username": credentials.username,
        "password": credentials.password
    }
    login_url = "https://train.mantisx.com/verify"
    response = network_util.get_session().post(login_url, headers=network_util.get_base_headers(), json=login_payload, timeout=30)

    if response.status_code == 200 and response.json().get("success"):
        logging.info("Login successful!")

        raw_data = response.json()
        return UserData(
            user_pk=raw_data["user_pk"],
            username=raw_data["username"],
            email=raw_data["email"],
            user_secret_key=raw_data["user_secret_key"]
        )
    else:
        logging.error("Login failed with status code: %s", response.status_code)
        raise RuntimeError(f"Login failed with status code: {response.status_code}")
