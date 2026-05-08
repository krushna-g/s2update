# Deploy S2Digital on Render

This project includes a `render.yaml` Blueprint for a simple Render web service.

## 1. Push the project to GitHub

```powershell
git add .
git commit -m "Add Render deployment files"
git push
```

## 2. Create the Render service

1. Open Render Dashboard.
2. Click **New**.
3. Click **Blueprint**.
4. Connect your GitHub repository.
5. Select the branch that contains `render.yaml`.
6. Enter an `ADMIN_KEY` value when Render asks for it.
7. Deploy the Blueprint.

Render will use:

```text
Build Command: python -m pip install --upgrade pip && python -m pip install -r requirements.txt
Start Command: python -m flask --app run.py init-db && gunicorn run:app --bind 0.0.0.0:$PORT
```

## 3. Manual Render setup

If you do not use the Blueprint, create a Render **Web Service** manually:

```text
Runtime: Python
Build Command: python -m pip install --upgrade pip && python -m pip install -r requirements.txt
Start Command: python -m flask --app run.py init-db && gunicorn app:app --bind 0.0.0.0:$PORT
```

Add these environment variables:

```text
S2Digital_CONFIG=S2Digital.config.ProdConfig
SECRET_KEY=<generate a strong secret>
ADMIN_KEY=<your admin password/key>
```

## Important note about SQLite on Render Free

The current app uses SQLite. Render Free web services use an ephemeral filesystem, so saved contact form entries can be lost after a restart or redeploy.

For a demo website, this is okay. For production, move the database to Render Postgres.
