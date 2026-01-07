
# Notes App

A Note Taking application built with **Django** (backend) and **Next.js** (frontend) that allows users to create, update, and delete notes with categories. This project also handles user authentication.

---

## Table of Contents

1. [Features](#features)  
2. [Technologies](#technologies)  
3. [Prerequisites](#prerequisites)  
4. [Setup Instructions](#setup-instructions)  
5. [Running the Project](#running-the-project)  
6. [Folder Structure](#folder-structure)  
7. [Notes](#notes)

---

## Features

- User registration and login
- Add, edit, and delete notes
- Categorize notes (Random Thoughts, School, Personal)
- Filter notes by category
- Responsive frontend with Next.js
- Backend API with Django REST Framework

---

## Technologies

- **Backend:** Django, Django REST Framework  
- **Frontend:** Next.js, React  
- **Database:** SQLite (default, can switch to PostgreSQL)  
- **Other:** Fetch API, CSRF token handling

---

## Prerequisites

- Python 3.10+  
- Node.js 18+ and npm  
- Git  

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
cd frontend
npm run dev
```

3. Open your browser at [http://localhost:3000](http://localhost:3000)

---

## Notes

* **Migrations:** Only include essential migrations. You can skip pushing `__pycache__` or the virtual environment folder.
* **CSRF:** Frontend is configured to handle CSRF cookies for Django authentication.
* **Dependencies:** Ensure `requirements.txt` is up-to-date. If you install new packages, run:

```bash
pip freeze > backend/requirements.txt
```

