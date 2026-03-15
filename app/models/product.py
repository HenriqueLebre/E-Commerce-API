from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    category = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    active = Column(Boolean, nullable=False, default=True)
    datecreation = Column(DateTime, nullable=False, default=func.now())
    dateupdated = Column(DateTime, nullable=True, onupdate=func.now())
    datedeactivated = Column(DateTime, nullable=True)