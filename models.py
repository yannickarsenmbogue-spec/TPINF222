from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    category = Column(String, nullable=True)
    tags = Column(String, nullable=True)  # stocké sous forme "tag1,tag2"