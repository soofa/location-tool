from sqlalchemy import Column, Integer, String, Text, DateTime, text
from sqlalchemy.dialects import postgresql
import datetime
from location_tool.database import Base

class BoundingBox(Base):
    __tablename__ = 'bounding_boxes'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True),
                        nullable=False,
                        server_default=text("select current_timestamp at time zone 'UTC'")
                        )
    updated_at = Column(DateTime(timezone=True),
                        nullable=False,
                        server_default=text("(select current_timestamp at time zone 'UTC')"),
                        onupdate=text("(select current_timestamp at time zone 'UTC')")
                        )
    name = Column(Text, nullable=False)
    state = Column(Text, nullable=False)
    coordinates = Column(postgresql.JSON, nullable=False)
    samples = Column(Text)
    googlescores = Column(Text)
    googletags = Column(Text)

    def __init__(self, name=None, state='created', coordinates=None, samples=None):
        self.name = name
        self.state = state
        self.coordinates = coordinates
        self.samples = samples
