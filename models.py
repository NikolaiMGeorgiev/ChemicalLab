from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)
    bodyfat = Column(Float)

class DiaryLog(Base):
    __tablename__ = 'diary'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    chemical = Column(String)
    quantity = Column(Float)
    date = Column(DateTime)
