from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from .. import schemas, models
from ..database import SessionLocal

router = APIRouter(prefix="/api/articles", tags=["articles"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ArticleResponse, status_code=201)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    # Convertir liste de tags en chaîne
    tags_str = ",".join(article.tags) if article.tags else None
    db_article = models.Article(
        title=article.title,
        content=article.content,
        author=article.author,
        category=article.category,
        tags=tags_str
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

@router.get("/", response_model=List[schemas.ArticleResponse])
def list_articles(
    category: Optional[str] = Query(None, description="Filtrer par catégorie"),
    author: Optional[str] = Query(None, description="Filtrer par auteur"),
    date: Optional[str] = Query(None, description="Filtrer par date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Article)
    if category:
        query = query.filter(models.Article.category == category)
    if author:
        query = query.filter(models.Article.author == author)
    if date:
        try:
            dt = datetime.strptime(date, "%Y-%m-%d").date()
            query = query.filter(models.Article.date >= dt, models.Article.date < dt.replace(day=dt.day+1))
        except ValueError:
            raise HTTPException(status_code=400, detail="Format de date invalide, utilisez YYYY-MM-DD")
    articles = query.all()
    return articles

@router.get("/search", response_model=List[schemas.ArticleResponse])
def search_articles(query: str = Query(..., description="Texte à rechercher dans le titre ou le contenu"), db: Session = Depends(get_db)):
    articles = db.query(models.Article).filter(
        models.Article.title.contains(query) | models.Article.content.contains(query)
    ).all()
    return articles

@router.get("/category/{category}", response_model=List[schemas.ArticleResponse])
def get_by_category(category: str, db: Session = Depends(get_db)):
    articles = db.query(models.Article).filter(models.Article.category == category).all()
    return articles

@router.get("/date/{date}", response_model=List[schemas.ArticleResponse])
def get_by_date(date: str, db: Session = Depends(get_db)):
    try:
        dt = datetime.strptime(date, "%Y-%m-%d").date()
        articles = db.query(models.Article).filter(
            models.Article.date >= dt,
            models.Article.date < dt.replace(day=dt.day+1)
        ).all()
        return articles
    except ValueError:
        raise HTTPException(status_code=400, detail="Format de date invalide, utilisez YYYY-MM-DD")

@router.get("/{article_id}", response_model=schemas.ArticleResponse)
def get_article(article_id: int = Path(..., description="ID de l'article"), db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return article

@router.put("/{article_id}", response_model=schemas.ArticleResponse)
def update_article(
    article_id: int,
    article_update: schemas.ArticleUpdate,
    db: Session = Depends(get_db)
):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
   
    update_data = article_update.dict(exclude_unset=True)
    if "tags" in update_data and update_data["tags"] is not None:
        update_data["tags"] = ",".join(update_data["tags"])
    for key, value in update_data.items():
        setattr(article, key, value)
   
    db.commit()
    db.refresh(article)
    return article

@router.delete("/{article_id}", response_model=dict)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    db.delete(article)
    db.commit()
    return {"message": "Article supprimé avec succès", "id": article_id}