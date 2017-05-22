from sqlalchemy import Column, Integer, String, Text
from location_tool.database import Base

class BoundingBox(Base):
    __tablename__ = 'bounding_boxes'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    state = Column(Text, nullable=False)

    def __init__(self):
        pass
