
import pytest
from pydantic import ValidationError

from app.schemas.field import FieldCreate
from app.schemas.measurement import MeasurementInput


def test_negative_field_area_rejected():
    with pytest.raises(ValidationError):
        FieldCreate(
            field_name="Test Field",
            type="olive",
            area=-10,
        )


def test_invalid_sensor_id_rejected():
    with pytest.raises(ValidationError):
        MeasurementInput(
            sensor_id=-1,
            value=25.0,
            timestamp="2026-01-01T12:00:00Z",
            unit="C",
        )


@pytest.mark.parametrize("value", [
    float("nan"),
    float("inf"),
    float("-inf"),
])
def test_non_finite_measurement_rejected(value):
    with pytest.raises(ValidationError):
        MeasurementInput(
            sensor_id=1,
            value=value,
            timestamp="2026-01-01T12:00:00Z",
            unit="C",
        )


@pytest.mark.parametrize("area", [
    0,
    float("nan"),
    float("inf"),
])
def test_invalid_field_area_rejected(area):
    with pytest.raises(ValidationError):
        FieldCreate(
            field_name="Test Field",
            type="olive",
            area=area,
        )
