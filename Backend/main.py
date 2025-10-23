# Backend/main.py
# Group Project: CS3100 Encryption API
# Author: Vip Monty (Group 2)
# Description: Accepts input from the frontend, encrypts the message, stores it in SQLite,
# and allows retrieval (with decryption) by name.

from Backend.algorithm_package.string_encryption import encrypt_string, decrypt_string
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from Backend.db import Base, engine, get_db
from Backend.models import Message

# -------------------------------------------------------
# Initialize FastAPI app
# -------------------------------------------------------
app = FastAPI(title="CS3100 Encryption API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------
# Create database tables at startup
# -------------------------------------------------------
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# -------------------------------------------------------
# Root route (homepage)
# -------------------------------------------------------
@app.get("/")
def home():
    return {"message": "Welcome to the CS3100 Encryption API!"}

# -------------------------------------------------------
# Pydantic models for input/output
# -------------------------------------------------------
class MessageIn(BaseModel):
    name: str
    message: str

class MessageOut(BaseModel):
    id: int
    name: str
    encrypted_message: str
    key: str

# -------------------------------------------------------
# API routes
# -------------------------------------------------------

# Encrypt and store message
@app.post("/message", response_model=MessageOut)
def create_message(data: MessageIn, db: Session = Depends(get_db)):
    key, encrypted_text = encrypt_string(data.message)
    new_msg = Message(name=data.name, encrypted_message=encrypted_text, key=key)
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg

# Retrieve and decrypt message
@app.get("/message/{name}")
def get_message(name: str, db: Session = Depends(get_db)):
    msg = db.execute(select(Message).where(Message.name == name)).scalar_one_or_none()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")

    decrypted = decrypt_string(msg.key, msg.encrypted_message)
    return {"name": msg.name, "message": decrypted}
