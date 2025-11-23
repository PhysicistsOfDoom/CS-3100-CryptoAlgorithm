# Backend/main.py
# Group Project: CS3100 Encryption API
# Author: Vip Monty (Group 2)
# Description: Accepts input from the frontend, encrypts the message, stores it in SQLite,
# and allows retrieval (with decryption) by name.

import os
from datetime import timedelta
from Backend.algorithm_package.string_encryption import encrypt_string, decrypt_string
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from Backend.db import Base, engine, get_db
from Backend.models import Message, User
from Backend.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_user_by_username,
    get_user_by_email,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# -------------------------------------------------------
# Initialize FastAPI app
# -------------------------------------------------------
app = FastAPI(title="CS3100 Encryption API")

# -------------------------------------------------------
# SECURITY FIX: Rate Limiting - Prevents brute force and DoS attacks
# -------------------------------------------------------
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# -------------------------------------------------------
# SECURITY FIX: CORS Configuration - Fixed insecure allow_origins=["*"]
# Previously allowed any origin, now uses specific allowed origins from env var
# -------------------------------------------------------
# Get allowed origins from environment variable or use defaults
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # SECURITY FIX: Specific origins instead of "*"
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
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

# SECURITY FIX: Authentication models - Added for JWT-based authentication
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

# -------------------------------------------------------
# SECURITY FIX: Authentication routes - Added user registration and login
# -------------------------------------------------------

# SECURITY FIX: Authentication endpoint - User registration with rate limiting
@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")  # SECURITY FIX: Rate limiting prevents registration spam
def register(
    request: Request,
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    # Check if username already exists
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# SECURITY FIX: Authentication endpoint - Login with JWT token generation
@app.post("/token", response_model=Token)
@limiter.limit("10/minute")  # SECURITY FIX: Rate limiting prevents brute force attacks
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# SECURITY FIX: Authentication endpoint - Get current user info (requires auth)
@app.get("/me", response_model=UserResponse)
@limiter.limit("30/minute")  # SECURITY FIX: Rate limiting
def read_users_me(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Get current user information."""
    return current_user

# -------------------------------------------------------
# SECURITY FIX: API routes now require authentication
# Previously these endpoints were publicly accessible
# -------------------------------------------------------

# SECURITY FIX: Encrypt and store message - Now requires authentication
@app.post("/message", response_model=MessageOut)
@limiter.limit("20/minute")  # SECURITY FIX: Rate limiting
def create_message(
    request: Request,
    data: MessageIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # SECURITY FIX: Auth required
):
    """Create and encrypt a message (requires authentication)."""
    key, encrypted_text = encrypt_string(data.message)
    new_msg = Message(
        name=data.name,
        encrypted_message=encrypted_text,
        key=key,
        user_id=current_user.id  # SECURITY FIX: Link message to authenticated user
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg

# SECURITY FIX: Retrieve and decrypt message - Now requires authentication
@app.get("/message/{name}")
@limiter.limit("30/minute")  # SECURITY FIX: Rate limiting
def get_message(
    request: Request,
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # SECURITY FIX: Auth required
):
    """Retrieve and decrypt a message (requires authentication)."""
    msg = db.execute(select(Message).where(Message.name == name)).scalar_one_or_none()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Optional: Only allow users to access their own messages
    # Uncomment the following lines to enforce user-specific message access:
    # if msg.user_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Not authorized to access this message")

    decrypted = decrypt_string(msg.key, msg.encrypted_message)
    return {"name": msg.name, "message": decrypted}
