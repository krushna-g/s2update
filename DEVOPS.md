# S2Digital DevOps Guide

This project now has a basic DevOps setup:

- GitHub repository for source control
- GitHub Actions for automated tests
- Docker image for container deployment
- Docker Compose for local container running
- Render Blueprint for cloud deployment

## Local development

```powershell
cd "c:\s2 digital.in"
.\.venv\Scripts\activate
pip install -r requirements.txt
flask --app run.py init-db
python run.py
```

Open:

```text
http://localhost:5000
```

## Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Docker build

Install Docker Desktop first, then run:

```powershell
docker build -t s2digital .
```

## Docker run

```powershell
docker run --rm -p 5000:5000 `
  -e S2Digital_CONFIG=S2Digital.config.ProdConfig `
  -e SECRET_KEY=change-this-secret `
  -e ADMIN_KEY=change-this-admin-key `
  s2digital
```

Open:

```text
http://localhost:5000
```

## Docker Compose

```powershell
docker compose up --build
```

Stop:

```powershell
docker compose down
```

Remove the SQLite volume:

```powershell
docker compose down -v
```

## GitHub Actions

The workflow file is:

```text
.github/workflows/test.yml
```

On every push or pull request it will:

1. Install Python dependencies
2. Run `pytest -q`
3. Build the Docker image

## Render deployment

Render uses:

```text
render.yaml
```

Push changes to GitHub, then in Render click:

```text
Manual Deploy > Deploy latest commit
```

## Recommended DevOps learning order

1. Git and GitHub
2. Python virtual environments
3. Pytest
4. GitHub Actions
5. Docker
6. Docker Compose
7. Render deployment
8. Logs and monitoring
9. PostgreSQL for production database
