from app.core.base import Base
from app.core.database import engine


from app.models import User, Field, Sensor, Measurement, Alert


Base.metadata.create_all(bind=engine)

print("Tables created successfully!")