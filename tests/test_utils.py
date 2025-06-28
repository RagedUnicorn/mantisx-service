import pytest
from datetime import datetime
from models.drill_type import DrillType
from models.session import Session
from models.session_extras import SessionExtras
from models.firearm import Firearm
from models.drill_settings import DrillSettings
from utils.filter import filter_sessions_by_drill


class TestUtils:
    """Test cases for utility functions"""

    def _create_test_session(self, pk: int, drill_name: str) -> Session:
        """Helper method to create a test session"""
        return Session(
            pk=pk,
            date=datetime.now(),
            user_pk=1,
            username="test_user",
            time_stamp=123456.0,
            right_handed=True,
            right_handed_display="Right",
            fire_type=1,
            fire_type_display="Live Fire",
            gun_type=1,
            gun_type_display="Pistol",
            average_score=85.5,
            stamp="test_stamp",
            drill_id=1,
            drill_name=drill_name,
            score_bars=5,
            time_bars=3,
            time_display="2.5s",
            deleted=False,
            shot_count=10,
            notes="Test notes",
            manual_score=0,
            course_number=1,
            extras=SessionExtras(
                hardware="Test Hardware",
                drill_settings=DrillSettings(repeat_count=1),
                offsetRoll=0.0,
                offsetPitch=0.0
            ),
            comments=[],
            firearm=Firearm(make="Test", model="Test", caliber="9mm"),
            gun_display="Test Gun",
            shots=[]
        )

    def test_filter_sessions_by_drill_with_matching_sessions(self):
        """Test filtering sessions with matching drill types"""
        # Create test sessions
        session1 = self._create_test_session(1, DrillType.HOLSTER_DRAW_ANALYSIS)
        session2 = self._create_test_session(2, DrillType.HOLSTER_DRAW_ANALYSIS)
        session3 = self._create_test_session(3, "Other Drill")  # Different drill type

        sessions = [session1, session2, session3]

        result = filter_sessions_by_drill(sessions, DrillType.HOLSTER_DRAW_ANALYSIS)

        assert result == [1, 2]
        assert len(result) == 2

    def test_filter_sessions_by_drill_no_matches(self):
        """Test filtering sessions with no matching drill types"""
        # Create test sessions with different drill types
        session1 = self._create_test_session(1, "Other Drill 1")
        session2 = self._create_test_session(2, "Other Drill 2")

        sessions = [session1, session2]

        result = filter_sessions_by_drill(sessions, DrillType.HOLSTER_DRAW_ANALYSIS)

        assert result == []
        assert len(result) == 0

    def test_filter_sessions_by_drill_empty_list(self):
        """Test filtering empty sessions list"""
        sessions = []

        result = filter_sessions_by_drill(sessions, DrillType.HOLSTER_DRAW_ANALYSIS)

        assert result == []
        assert len(result) == 0
