# lostfound

lostfound is a Django-based Lost and Found web application where users can report missing items, publish found items, claim ownership with proof, and receive status notifications.

## Project Highlights

- User authentication (register, login, logout)
- Create and browse lost/found item listings
- Item filtering and search
- Claim workflow for ownership requests
- Admin moderation through Django admin
- Notification support for user actions and status updates
- Media upload support for item images and claim proof

## Tech Stack

- Python 3.13
- Django 6.x
- SQLite (default development database)
- HTML templates + Django template engine

## Folder Structure

```text
lostfound/
  manage.py                   # Root launcher for the nested Django project
  README.md
  .gitignore
  lostfound/
    manage.py                 # Original Django manage.py
    db.sqlite3
    core/
      models.py               # Main domain models (items, claims, notifications)
      views.py                # App logic and request handlers
      forms.py                # Django forms for items/claims/auth
      urls.py                 # App routes
      templates/              # UI templates
    lostfound/
      settings.py             # Django settings
      urls.py                 # Root URL config
      asgi.py
      wsgi.py
    media/
      items/
```

## End-to-End Flow

1. User Authentication:
   - A user registers or logs in.
   - Session-based authentication protects user-specific pages.

2. Item Reporting:
   - User posts an item as Lost or Found with details (title, category, location, date, description, image).
   - Item data is persisted in the database.

3. Discovery and Matching:
   - Users browse the dashboard/home listings.
   - Filters and search help narrow down relevant items.

4. Claim Submission:
   - For a found item, the rightful owner submits a claim request.
   - Claim includes a message/proof to verify ownership.

5. Review and Resolution:
   - Item owner/admin reviews claim details.
   - Claim can be accepted/rejected and item status is updated.

6. Notifications:
   - Users receive notifications for claim actions and key updates.

## Local Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Run migrations.
5. Start the dev server.

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install django pillow
python manage.py migrate
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## Useful Commands

```powershell
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Publishing and Keeping GitHub Updated

This project is set up so every change becomes visible on GitHub after push.

### Initial publish

```powershell
git init
git branch -M main
git add .
git commit -m "Initial commit: lostfound project"
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

### Regular update flow

```powershell
git add .
git commit -m "Describe your update"
git push
```

If you follow this commit+push flow, all additions/updates are reflected on GitHub.

## Notes

- Keep secrets and private configuration out of source control.
- For production, use PostgreSQL/MySQL and a production-ready server setup.
- This repository keeps project naming consistent as `lostfound` for clarity.
