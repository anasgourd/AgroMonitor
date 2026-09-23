from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.repositories.alert_repository import AlertRepository
from datetime import datetime

class AlertService:
    def __init__(self, db: Session):
        self.repository = AlertRepository(db)

    def get_user_alerts(
        self,
        user_id: int
    ) -> list[Alert]:

        return self.repository.get_by_user_id(user_id)
    

    def get_field_alerts(
        self,
        field_id: int
    ) -> list[Alert]:

        return self.repository.get_by_field_id(field_id)
    
    def get_alert(
        self,
        alert_id: int
    ) -> Alert | None:
        return self.repository.get_by_id(alert_id)
    
    def create_alert(
        self,
        measurement_id: int,
        message: str,
        timestamp: datetime
    ) -> Alert:

        return self.repository.create(
            measurement_id,
            message,
            timestamp
        )