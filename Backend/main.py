from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text, select

from .db import Base, engine, get_db
from .models import Item
from .schemas import ItemCreate, ItemOut

app = FastAPI(title="Starter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables at boot
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"ok": True}

# ---- Items (CRUD-lite) ----
@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(body: ItemCreate, db: Session = Depends(get_db)):
    # Pydantic validation will automatically check for SQL injection patterns
    item = Item(title=body.title, description=body.description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get("/items", response_model=list[ItemOut])
def list_items(db: Session = Depends(get_db)):
    items = db.execute(select(Item).order_by(Item.id)).scalars().all()
    return items

@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    return item
