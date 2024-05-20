# Commands Documentation

## Overview
This document describes the available commands for the Django project integrated with Celery and their usage.

## General Django Commands

### `runserver`
Starts the Django development server.

**Usage:**
```
python manage.py runserver 80
```

### `makemigrations`
Creates new migrations based on the changes detected to your models.

**Usage:**
```
python manage.py makemigrations ig_scraper
```
### `migrate`
Applies database migrations.

**Usage:**
```
python manage.py migrate
```
## User Management

### `createsuperuser`
Creates a new superuser.

**Usage:**
```
python manage.py createsuperuser
```
## Celery Commands

### `celery -A <project_name> worker`
Starts the Celery worker.

**Usage For This Project:**
```
celery -A ig_scraper worker --loglevel=info --pool=solo
```

### `celery -A <project_name> beat`
Starts the Celery beat scheduler.

**Usage For This Project:**
```
celery -A ig_scraper beat -l info
```