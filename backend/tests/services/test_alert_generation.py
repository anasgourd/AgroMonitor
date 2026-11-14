from datetime import datetime
from unittest.mock import MagicMock

from app.services.alert_service import AlertService


def test_create_alert():
    db = MagicMock()
    service = AlertService(db)

    service.repository.create = MagicMock()

    timestamp = datetime(2026, 9, 23, 14, 0)

    service.create_alert(
        measurement_id=1,
        message="Anomaly detected",
        timestamp=timestamp
    )

    service.repository.create.assert_called_once_with(
        1,
        "Anomaly detected",
        timestamp
    )