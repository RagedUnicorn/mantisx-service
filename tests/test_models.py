import pytest
from models.drill_type import DrillType


class TestModels:
    """Test cases for model classes"""

    def test_drill_type_enum_values(self):
        """Test DrillType enum has expected values"""
        assert DrillType.HOLSTER_DRAW_ANALYSIS == "Holster Draw Analysis"
        assert DrillType.HOLSTER_DRAW_ANALYSIS.value == "Holster Draw Analysis"

    def test_drill_type_string_conversion(self):
        """Test DrillType can be used as string"""
        drill_type = DrillType.HOLSTER_DRAW_ANALYSIS
        # Test the value, not the string representation
        assert drill_type.value == "Holster Draw Analysis"
        assert drill_type == "Holster Draw Analysis"

    def test_drill_type_equality(self):
        """Test DrillType equality comparison"""
        drill1 = DrillType.HOLSTER_DRAW_ANALYSIS
        drill2 = DrillType.HOLSTER_DRAW_ANALYSIS

        assert drill1 == drill2
        assert drill1 == "Holster Draw Analysis"
