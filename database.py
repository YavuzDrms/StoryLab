from pydantic import BaseModel
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
import sqlite3

engine = create_engine("sqlite:///./database.db", connect_args={"check_same_thread": False})
local_session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class MessageDB(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    prompt = Column(String)
    response = Column(Text)
    date_time = Column(DateTime, default=datetime.datetime.now)

Base.metadata.create_all(engine)
    
# Model of every message
# User message, AI response and date, time
class DataModel():
    prompt: str
    date_time: datetime.datetime
    response: str
    def __init__(self, p: str, dt: datetime.datetime, r: str):
        self.prompt = p
        self.date_time = dt
        self.response = r

def get_date() -> datetime.datetime:
    return datetime.datetime.now()

def log_data(data: DataModel):
    print(f"User promt: {data.prompt}\nDate and time: {data.date_time}\nResponse: {data.response}")
    
    db = local_session()
    db.add(MessageDB(
        prompt=data.prompt,
        response=data.response,
        date_time=data.date_time
    ))
    db.commit()
    db.close()

def clear_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM messages")
    
    try:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='messages'")
    except sqlite3.OperationalError:
        pass
    
    conn.commit()
    conn.close()
    print("Database succesfuly cleared")