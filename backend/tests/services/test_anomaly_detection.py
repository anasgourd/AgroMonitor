from app.services.anomaly_detection.anomaly_detection_service import (
    AnomalyDetectionService,
)
from app.services.anomaly_detection.threshold_strategy import (
    ThresholdAnomalyDetectionStrategy,
)


def test_threshold_strategy_detects_anomaly():
    strategy = ThresholdAnomalyDetectionStrategy()

    assert strategy.is_anomalous(81) is True


def test_threshold_strategy_accepts_normal_value():
    strategy = ThresholdAnomalyDetectionStrategy()

    assert strategy.is_anomalous(80) is False


def test_anomaly_detection_service_uses_strategy():
    strategy = ThresholdAnomalyDetectionStrategy()
    service = AnomalyDetectionService(strategy)

    assert service.is_anomalous(81) is True
    assert service.is_anomalous(70) is False