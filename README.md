# S2Digital — Simple Flask Website

Minimal Flask app for a company site with pages: Home, About, Products, Services, Contact and a simple chatbot + admin view for contact inquiries.

## Features
- App factory pattern
- Blueprints: `main` (pages + contact) and `chat` (chat API)
- SQLite via Flask-SQLAlchemy
- Simple admin view protected by a query key
- Environment-aware configuration (Dev / Test / Prod)

## Prerequisites
- macOS with Python 3 installed (use `python3`)
- Git (optional)

## Quick setup (project root: /Users/sachinlande/S2Digital)
1. Create & activate venv
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# default dev DB: S2Digital_dev.db
export DATABASE_URL=sqlite:///S2Digital_dev.db
# change admin key (default is "changeme")
export ADMIN_KEY=mysupersecret
# select config (optional)
export S2Digital_CONFIG=S2Digital.config.ProdConfig

##
Run tests:
activate your .venv
pip install -r requirements.txt
pytest -q


##
# activate venv
source .venv/bin/activate

# from project root - to have latest added db changes 
source .venv/bin/activate
rm -f S2Digital_dev.db S2Digital.db
flask --app run.py init-db
python run.py
# run server
python run.py