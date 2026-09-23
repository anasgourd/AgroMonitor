from app.services.anomaly_detection.strategy import AnomalyDetectionStrategy


class ThresholdAnomalyDetectionStrategy(AnomalyDetectionStrategy):

    def is_anomalous(self, value: float) -> bool:
        return value > 80