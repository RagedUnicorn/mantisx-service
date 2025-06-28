import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch
import tempfile
import json

from models.drill_type import DrillType
from models.session_response import SessionResponse
from models.session import Session
from main import save_session_to_file, get_session_data, parse_arguments


class TestMain:
    """Test cases for main.py functions"""

    def test_save_session_to_file(self):
        """Test saving session data to file"""
        # Create a mock session response
        mock_session = Mock()
        mock_session.date = datetime(2025, 6, 27)
        mock_session.pk = 12345

        mock_session_response = Mock(spec=SessionResponse)
        mock_session_response.session = mock_session

        # Use temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)

            # Mock the datetime.fromisoformat call
            with patch('main.datetime') as mock_datetime:
                mock_datetime.fromisoformat.return_value.strftime.return_value = "2025_06_27"

                # Mock json.dump to avoid actual file writing complexity
                with patch('main.json.dump') as mock_json_dump:
                    result_path = save_session_to_file(mock_session_response, output_dir)

                    # Verify the filename format
                    expected_filename = output_dir / "2025_06_27_session_12345.json"
                    assert result_path == expected_filename

                    # Verify json.dump was called
                    mock_json_dump.assert_called_once()

    @patch('main.get_session')
    def test_get_session_data(self, mock_get_session):
        """Test fetching session data"""
        mock_user_data = {"user": "test"}
        session_pk = 12345
        mock_response = Mock(spec=SessionResponse)
        mock_get_session.return_value = mock_response

        result = get_session_data(mock_user_data, session_pk)

        mock_get_session.assert_called_once_with(mock_user_data, session_pk)
        assert result == mock_response

    def test_parse_arguments_default(self):
        """Test parsing arguments with defaults"""
        import sys
        original_argv = sys.argv
        try:
            sys.argv = ['main.py']
            args = parse_arguments()

            assert args.days_back == 1
            assert args.start_date is None
            assert args.end_date is None
            assert args.output_dir == 'output_data'
        finally:
            sys.argv = original_argv

    def test_parse_arguments_with_days_back(self):
        """Test parsing arguments with days_back"""
        import sys
        original_argv = sys.argv
        try:
            sys.argv = ['main.py', '--days-back', '7']
            args = parse_arguments()

            assert args.days_back == 7
        finally:
            sys.argv = original_argv

    def test_parse_arguments_with_dates(self):
        """Test parsing arguments with date range"""
        import sys
        original_argv = sys.argv
        try:
            sys.argv = ['main.py', '--start-date', '25/06/2025', '--end-date', '28/06/2025']
            args = parse_arguments()

            assert args.start_date == '25/06/2025'
            assert args.end_date == '28/06/2025'
        finally:
            sys.argv = original_argv

    def test_parse_arguments_invalid_date_format(self):
        """Test parsing arguments with invalid date format"""
        import sys
        original_argv = sys.argv
        try:
            sys.argv = ['main.py', '--start-date', '2025-06-25']  # Wrong format
            with pytest.raises(SystemExit):
                parse_arguments()
        finally:
            sys.argv = original_argv
