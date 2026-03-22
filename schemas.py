from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

class ArticleBase(BaseModel):
    title: str
    content: str
    author: str
    category: Optional[str] = None
    tags: Optional[List[str]] = None

class ArticleCreate(ArticleBase):
    @validator('title')
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Le titre ne peut pas être vide')
        return v.strip()

    @validator('author')
    def author_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("L'auteur est obligatoire")
        return v.strip()

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None

    @validator('title')
    def title_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Le titre ne peut pas être vide')
        return v.strip() if v else v

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
    date: datetime
    category: Optional[str] = None
    tags: Optional[List[str]] = None

    class Config:
        from_attributes = True
    @validator('tags', pre=True, always=True)
    def parse_tags(cls, v):
        if isinstance(v, str):
            return v.split(',') if v else []
        return v