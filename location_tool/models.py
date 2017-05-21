from sqlalchemy import Column, Integer, String
from location_tool.database import Base

class BoundingBox(Base):
    __tablename__ = 'bounding_boxes'
    id = Column(Integer, primary_key=True)

    def __init__(self):
        pass
