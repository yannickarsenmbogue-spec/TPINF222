# TPINF222
 Blog API - Backend de gestion d'articles

API REST développée avec **FastAPI** et **SQLite** pour la gestion d'un blog simple. Elle permet de créer, lire, modifier, supprimer et rechercher des articles.

## Fonctionnalités

- Créer un article (titre, contenu, auteur, date, catégorie, tags)
- Lire tous les articles avec filtrage (catégorie, auteur, date)
- Lire un article par son ID
- Modifier un article (titre, contenu, catégorie, tags)
- Supprimer un article
- Rechercher un article par mot-clé dans le titre ou le contenu
- Endpoints supplémentaires : articles par catégorie, par date
- Validation des entrées (titre non vide, auteur obligatoire)
- Codes HTTP appropriés (200, 201, 400, 404, 500)
- Séparation claire des routes, contrôleurs et modèles
- Documentation interactive Swagger (via `/docs`)

## Technologies

- Python 3.9+
- FastAPI
- SQLAlchemy (ORM)
- SQLite
- Uvicorn (serveur ASGI)

## Installation
telecharger les dependances ce trouvant dans le fichier requirements.txt
utiliser les codes python -m venv venv pour creer un environement virtuel et source venv/bin/activate pour activer votre environement
lancer l'API avec la commande uvicorn app.main:app --reload
L'API sera accessible sur http://localhost8000 et la documentation SWagger sur http://localhost8000/docs
