# Backend/models.py
from sqlalchemy import Column, Integer, String
from Backend.db import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    encrypted_message = Column(String, nullable=False)
    key = Column(String, nullable=False)
    user_id = Column(Integer, nullable=True)  # SECURITY FIX: Link messages to users for authorization

# SECURITY FIX: User model - Added for authentication system
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)  # SECURITY FIX: Passwords stored as hashes, not plaintext
