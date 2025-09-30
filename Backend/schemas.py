from pydantic import BaseModel

class ItemCreate(BaseModel):
    title: str
    description: str | None = None

class ItemOut(ItemCreate):
    id: int
