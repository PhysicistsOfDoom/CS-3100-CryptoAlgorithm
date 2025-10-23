from sqlalchemy import Column, Integer, String
from Backend.db import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    encrypted_message = Column(String, nullable=False)
    key = Column(String, nullable=False)

