from abc import ABC, abstractmethod


class AnomalyDetectionStrategy(ABC):

    @abstractmethod
    def is_anomalous(self, value: float) -> bool:
        pass