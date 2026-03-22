from fastapi import FastAPI
from .database import engine
from . import models
from .routers import articles

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API", description="API de gestion d'articles de blog", version="1.0.0")

app.include_router(articles.router)

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Blog. Consultez /docs pour la documentation."}