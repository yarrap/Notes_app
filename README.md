# Notes App

A Note Taking application built with **Django** (backend) and **Next.js** (frontend) that allows users to create, update, and delete notes with categories. This project also handles user authentication.

---

## App Screenshots

### Login Page:

![Alt text](pictures/image-4.png)

### Registration Page:

![Alt text](pictures/image-1.png)

### Main Page:

![Alt text](pictures/image-2.png)

### Single Note Page:

![Alt text](pictures/image-3.png)

---

## Table of Contents

1. [Features](#features)
2. [Technologies](#technologies)
3. [Prerequisites](#prerequisites)
4. [Setup Instructions](#setup-instructions)
5. [Running the Project](#running-the-project)
6. [Folder Structure](#folder-structure)
7. [Summary & Design Decisions](#summary--design-decisions)
8. [AI Usage](#ai-usage)
9. [Notes](#notes)

---

## Features

* User registration and login
* Add, edit, and delete notes
* Categorize notes (Random Thoughts, School, Personal)
* Filter notes by category
* Responsive frontend with Next.js
* Backend API with Django REST Framework

---

## Technologies

* **Backend:** Django, Django REST Framework
* **Frontend:** Next.js, React
* **Database:** SQLite (default, can switch to PostgreSQL)
* **Other:** Fetch API, CSRF token handling

---

## Prerequisites

* Python 3.10+
* Node.js 18+ and npm
* Git

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yarrap/Notes_app.git
cd Notes_app
```

---

### 2. Setup Backend (Django)

#### a) Create a Python virtual environment

```bash
python -m venv env
```

#### b) Activate the virtual environment

* **Mac/Linux:**

```bash
source env/bin/activate
```

#### c) Install dependencies

```bash
pip install -r backend/requirements.txt
```

#### d) Apply migrations

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

#### e) (Optional) Create a superuser

```bash
python manage.py createsuperuser
```

#### f) Start Django server

```bash
python manage.py runserver
```

Backend will run at `http://localhost:8000/`.

---

### 3. Setup Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at `http://localhost:3000/`.

---

## Running the Project

1. Start the **backend**:

```bash
cd backend
source ../env/bin/activate  # if not already activated
python manage.py runserver
```

2. Start the **frontend**:

```bash
cd frontend/notes-frontend
npm run dev
```

3. Open your browser at [http://localhost:3000](http://localhost:3000)

---

## Folder Structure

```
backend/
│
├── notes_app/                 # Main Django app
│   ├── migrations/            # Database migrations
│   ├── models.py              # Models
│   ├── serializers.py         # DRF serializers
│   ├── views.py               # API views
│   ├── urls.py                # App URLs
│   └── tests.py               # Unit tests
│
├── notes_app_project/         # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── manage.py                  # Django CLI

frontend/
├── notes-frontend/            # Next.js frontend
│   ├── pages/                 # Pages
│   ├── components/            # React components
│   └── styles/                # CSS / Tailwind styles
└── package.json
```

---

## Summary & Design Decisions

* **Backend:** I used Django and Django REST Framework to structure a clean, scalable API. Models were designed to handle notes, categories, and users efficiently. API endpoints follow REST principles for consistency.
* **Frontend:** Next.js was chosen for a responsive, component-based UI. Pages and components were organized to match the Figma design for simplicity and maintainability.
* **Integration:** Fetch API is used to interact with the Django backend, handling CSRF tokens for authentication.
* **Modularity:** Code is split into clear modules, making it easy to extend with features like additional categories or search in the future.

**Overall Process:**
I started by setting up the Django backend and creating the models, serializers, and views. Then I built the Next.js frontend, mapping UI components to backend API endpoints. The app was tested at each stage to ensure smooth integration. Screenshots were taken to verify functionality.

---

## AI Usage

**Backend**: All core logic including models, serializers, views, and API endpoints were written by me, referencing official Django documentation and online resources. AI tools (Claude & GPT) were used to suggest minor improvements or optimizations, which I carefully reviewed and adapted before integrating. The main design, architecture, and implementation decisions were fully human-written.

**Frontend**: For the frontend, I showed Claude the screenshots from the Figma design to get guidance on structuring and coding Next.js components, and on integrating them with the Django backend. All AI suggestions were carefully reviewed and modified manually to ensure correctness and adherence to the design.

---

## Notes

* **Migrations:** Only include essential migrations. Skip `__pycache__` or the virtual environment folder.
* **CSRF:** Frontend handles CSRF cookies for Django authentication.
* **Dependencies:** Ensure `requirements.txt` is up-to-date. If you install new packages:

```bash
pip freeze > backend/requirements.txt
```


