from sqlalchemy import Column, Integer, Float, String, DateTime, func
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

class Vendors(Base):
    __tablename__ = 'vendors'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Chats(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    vendor_id = Column(Integer)

class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    content = Column(String)
    sent_time = Column(DateTime, default=func.now())
    sender = Column(String)
    read = Column(Integer, default=0)

class DiaryLog(Base):
    __tablename__ = 'diary'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    chemical = Column(String)
    quantity = Column(Float)
    date = Column(DateTime)

class LabHistory(Base):
    __tablename__ = 'lab_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    substance = Column(String)
    muscle_mass = Column(Integer)
    body_fat = Column(Integer)
    energy = Column(Integer)
    stength = Column(Integer)
    cancer = Column(Integer)
    impotence = Column(Integer)
    diabetes = Column(Integer)
    heart_disease = Column(Integer)