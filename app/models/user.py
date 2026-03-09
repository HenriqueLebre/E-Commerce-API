from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    # Toda tabela precisa de uma primary key
    id = Column(Integer, primary_key=True, index=True)

    # Colunas normais
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    number = Column(String, nullable=False, unique=True)
    active = Column(bool, nullable=False, default=True)
    datecreation = Column(DateTime, nullable=False, default=func.now())
    dateatualization = Column(DateTime, nullable=True)
    datedesactivted = Column(DateTime, nullable=True)
    isadmin = Column(bool, nullable=False, default=False)