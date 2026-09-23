from app.services.anomaly_detection.strategy import AnomalyDetectionStrategy


class AnomalyDetectionService:

    def __init__(self, strategy: AnomalyDetectionStrategy):
        self.strategy = strategy

    def is_anomalous(self, value: float) -> bool:
        return self.strategy.is_anomalous(value)