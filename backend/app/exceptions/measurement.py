class SensorNotFoundError(Exception):
    pass


class InactiveSensorError(Exception):
    pass


class FutureMeasurementTimestampError(Exception):
    pass