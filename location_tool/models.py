from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects import postgresql
from location_tool.database import Base

class BoundingBox(Base):
    __tablename__ = 'bounding_boxes'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    state = Column(Text, nullable=False)
    coordinates = Column(postgresql.JSON, nullable=False)

    def __init__(self):
        pass
