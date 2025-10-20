
from pydantic import BaseModel, validator
from typing import Optional, ClassVar, List

class ItemCreate(BaseModel):
    title: str
    description: Optional[str] = None

    # Mark this as a ClassVar so Pydantic ignores it as a field
    DANGEROUS_CHARS: ClassVar[List[str]] = [
        "'", '"', ';', '--', '/*', '*/', 'xp_', 'sp_', 'exec', 'execute',
        'union', 'select', 'insert', 'update', 'delete', 'drop', 'create', 'alter'
    ]

    @validator('title')
    def sanitize_title(cls, v):
        if v is None:
            return v
        v_lower = v.lower()
        for char in cls.DANGEROUS_CHARS:
            if char in v_lower:
                raise ValueError(f"Title contains potentially dangerous content: {char}")
        return v

    @validator('description')
    def sanitize_description(cls, v):
        if v is None:
            return v
        v_lower = v.lower()
        for char in cls.DANGEROUS_CHARS:
            if char in v_lower:
                raise ValueError(f"Description contains potentially dangerous content: {char}")
        return v


class ItemOut(ItemCreate):
    id: int

