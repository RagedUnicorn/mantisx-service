import logging
import sys
import os
import requests
import json
import argparse
import network.network_util as network_util

from pathlib import Path
from datetime import datetime
from network.authenticate import login
from network.get_session_history import get_sessions_history
from network.get_session import get_session
from utils.filter import filter_sessions_by_drill
from utils.enhanced_json_encoder import EnhancedJSONEncoder
from models.drill_type import DrillType
from models.session_response import SessionResponse

# logging levels
# CRITICAL = 50
# FATAL = CRITICAL
# ERROR = 40
# WARNING = 30
# WARN = WARNING
# INFO = 20
# DEBUG = 10
# NOTSET = 0
logging.basicConfig(
    stream=sys.stdout,
    level=int(os.environ.get("MANTISX_SERVICE_LOG_LEVEL", logging.INFO)),
    format="%(asctime)s - %(levelname)s - %(message)s",
)

session = requests.Session()
network_util.set_session(session)


def save_session_to_file(session_data: SessionResponse, output_dir: Path) -> Path:
    """
    Saves the session data to a JSON file in the specified output directory.
    The filename includes the session date and pk.
    """
    session_date = datetime.fromisoformat(session_data.session.date.isoformat()).strftime("%Y_%m_%d")
    filename = output_dir / f"{session_date}_session_{session_data.session.pk}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(session_data, f, indent=2, cls=EnhancedJSONEncoder)

    return filename


def get_session_data(user_data, session_pk) -> SessionResponse:
    """
    Fetches session data for a given session primary key (pk).
    """
    logging.debug("Fetching session data for pk: %s", session_pk)
    return get_session(user_data, session_pk)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='MantisX Service')
    parser.add_argument('--days-back',
                        type=int,
                        default=1,
                        help='Number of days to look back for sessions (default: 1)')
    parser.add_argument('--start-date',
                        type=str,
                        help='Start date for session retrieval (format: DD/MM/YYYY, e.g., 25/06/2025)')
    parser.add_argument('--end-date',
                        type=str,
                        help='End date for session retrieval (format: DD/MM/YYYY, e.g., 28/06/2025). If only start-date is provided, end-date defaults to today')
    parser.add_argument('--output-dir',
                        type=str,
                        default='output_data',
                        help='Output directory for session files (default: output_sessions)')

    args = parser.parse_args()

    # Validation logic for date arguments
    if args.end_date and not args.start_date:
        parser.error("--end-date cannot be used without --start-date")

    if args.start_date or args.end_date:
        if args.days_back != 1:  # days_back was explicitly set
            logging.warning("--days-back takes priority over date range arguments. Ignoring --start-date and --end-date")
        else:
            # Validate date formats
            from datetime import datetime
            try:
                if args.start_date:
                    datetime.strptime(args.start_date, '%d/%m/%Y')
                if args.end_date:
                    datetime.strptime(args.end_date, '%d/%m/%Y')
            except ValueError as e:
                parser.error(f"Invalid date format. Use DD/MM/YYYY format: {e}")

    return args


def main():
    args = parse_arguments()
    
    try:
        user_data = login()
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        logging.error("Authentication failed: %s", e)
        sys.exit(1)

    try:
        if (args.start_date or args.end_date) and args.days_back == 1:
            session_history = get_sessions_history(user_data, start_date=args.start_date, end_date=args.end_date)
        else:
            session_history = get_sessions_history(user_data, days_back=args.days_back)
    except RuntimeError as e:
        logging.error("Failed to retrieve session history: %s", e)
        sys.exit(1)

    # gather all session pks for a specific drill type
    filtered_pks = filter_sessions_by_drill(session_history.sessions, DrillType.HOLSTER_DRAW_ANALYSIS)
    logging.debug("Filtered session PKs: %s", filtered_pks)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for pk in filtered_pks:
        try:
            session_data = get_session_data(user_data, pk)
            saved_path = save_session_to_file(session_data, output_dir)
            logging.debug("Saved session %s to %s", pk, saved_path)
        except Exception as e:
            logging.error("Failed to fetch or save session data for pk %s: %s", pk, e)


if __name__ == "__main__":
    main()
