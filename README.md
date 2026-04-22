# GoldLedger

GoldLedger is a clean Django web application for tracking personal gold jewelry records, their values, and related supporting documents.

## Stack

- Backend: Django
- Frontend: Django templates with Tailwind CSS and Preline via CDN
- Database: SQLite
- Architecture: multi-app Django project

## Features

- Django built-in authentication
- Dashboard with item counts, values, and missing document summaries
- Jewelry inventory CRUD
- Per-user item ownership and access control
- Document upload and management for bills, certificates, photos, and other files
- Basic automated tests
- Sample seeding command for local testing

## Apps

- `accounts` - login and root redirect behavior
- `core` - shared UUID and timestamp base models
- `inventory` - jewelry item models, forms, views, admin, and seed command
- `documents` - related document models and workflows
- `dashboard` - user summary and overview page

## Local setup

1. Create and activate a virtual environment.
2. Install dependencies.
3. Run migrations.
4. Create a superuser.
5. Start the development server.

Example commands:

```bash
python -m venv .venv
source .venv/bin/activate
pip install django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Seed sample data

The project includes a management command that creates sample jewelry items and generated document files for a specific user.

```bash
python manage.py seed_goldledger --username admin --count 20 --reset
```

This generates:

- 20 jewelry items
- photo-style SVG document previews
- sample bill documents
- sample certificate documents

## Run tests

```bash
python manage.py test
```

## Notes

- User data is ownership-scoped; logged-in users only access their own items and documents.
- Media files are stored locally for development.
- The current UI setup uses CDN assets for simplicity during development.
