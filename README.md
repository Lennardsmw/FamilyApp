# Familien-App

Eine Django-Web-App für Familienorganisation mit Einkaufsliste, Dashboard und mehr.

## Vorschau

| Login | Dashboard |
|-------|-----------|
| ![Login](assets/demo4.png) | ![Dashboard](assets/demo1.png) |

| Settings (Profilbild, Design, Passwort) | Settings (Familienmitglieder) |
|----------------------------------------|------------------------------|
| ![Settings 1](assets/demo2.png) | ![Settings 2](assets/demo3.png) |

| Einkaufsliste |
|---------------|
| ![Einkaufsliste](assets/demo0.png) |

## Features

- **Dashboard** – Zentrale Übersicht mit Kacheln für Einkaufsliste, Chat, Essensplan, Kalender
- **Einkaufsliste** – Gemeinsame Einkaufsliste für die Familie (App: `shopping`)
- **Profilbilder** – Upload mit Komprimierung und eindeutigen Dateinamen
- **Design-Modi** – Schwarz / Weiß / Colored (umstellbar in den Einstellungen)
- **Familienverwaltung** – Familienmitglieder hinzufügen und verwalten
- **Benutzerverwaltung** – Registrierung, Login, Passwort ändern

## Schnellstart

### 1. Repository klonen

```bash
git clone <repo-url>
cd FamilyApp
```

### 2. Virtualenv erstellen und aktivieren

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4. Datenbank initialisieren

```bash
python manage.py migrate
```

### 5. Entwicklungsserver starten

```bash
python manage.py runserver
```

Die App ist dann unter [http://127.0.0.1:8000](http://127.0.0.1:8000) erreichbar.

## Umgebungsvariablen (`.env`)

Erstelle eine `.env`-Datei im Projekt-Root für Production:

```env
SECRET_KEY=dein-geheimer-schlüssel
DEBUG=False
ALLOWED_HOSTS=deine-domain.de
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

Ohne `.env` läuft die App lokal mit SQLite und DEBUG-Modus.

## Deployment

### Statische Dateien sammeln

```bash
python manage.py collectstatic
```

### Mit Gunicorn starten

```bash
gunicorn familyapp.wsgi
```

## Tech-Stack

- **Backend:** Django 5.x, PostgreSQL / SQLite
- **Frontend:** Bootstrap 5.3, Eigenes CSS
- **Bildverarbeitung:** Pillow

## Projektstruktur

```
FamilyApp/
├── accounts/          # Benutzerverwaltung, Profilbilder, Einstellungen
├── familyapp/         # Django-Projekt-Konfiguration (settings, urls)
├── shopping/          # Einkaufslisten-App
├── mPanel/            # Familien-Management-Panel
├── media/             # Hochgeladene Dateien (Profilbilder)
├── static/            # Statische Dateien (CSS, Bilder)
└── staticfiles/       # Collectstatic-Ziel (wird beim Deployment erzeugt)
```

## Abhängigkeiten

- Django
- Pillow (Bildverarbeitung)
- django-environ & python-dotenv (Umgebungsvariablen)
- gunicorn (Production-Server)
- whitenoise (Statische Dateien in Production)
- psycopg2-binary (PostgreSQL-Anbindung)
