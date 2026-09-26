# 🏗️ DevSpace

A personal Django learning project built while exploring authentication, user management, posts, forms, OAuth, email verification, and other parts of the Django ecosystem.

> **Status:** learning project / experimental sandbox.  
> This repository is not intended to be production-ready.

## ✨ What is inside?

The project is a small web application centered around users and posts.

### Main functionality

- 👤 Custom Django user model
- 🔐 Authentication and login
- 🔑 Custom email authentication backend
- 🌐 Google OAuth2 authentication
- ✉️ Email verification flow
- 📝 Create, view, edit and manage posts
- 🖼️ Image uploads for posts
- 🔎 Post filtering
- 📄 Pagination
- 🛡️ Cloudflare Turnstile integration
- 🗄️ PostgreSQL database
- 🧰 Django admin
- 🐍 Django ORM
- 🧪 Django Extensions / IPython for development

## 🧠 What I was practicing

The main purpose of this project was to learn Django by building features instead of following only isolated examples.

Some of the topics explored here:

- Django project and application structure
- Models and relationships
- Custom user models
- Class-based views
- Generic Django views
- Forms and validation
- Authentication backends
- Login/logout flows
- OAuth2 with social-auth-app-django
- Custom authentication pipelines
- Email verification
- File and image uploads
- URL namespaces and reverse resolution
- Pagination and filtering
- Django middleware
- PostgreSQL integration

## 🛠️ Tech Stack

- **Python 3.13+**
- **Django 6**
- **PostgreSQL**
- **psycopg2**
- **django-extensions**
- **social-auth-app-django**
- **django-turnstile**
- **python-dotenv**
- **uv**

## 📁 Project Structure

~~~text
django-test-DEVSPACE/
│
├── DevSpace/
│   ├── DevSpace/             # Django project configuration
│   ├── posts/                # Posts application
│   ├── users/                # Custom user and authentication logic
│   ├── mail_verifications/   # Email verification functionality
│   ├── templates/            # Project templates
│   ├── media/                # Uploaded media
│   ├── fixtures/             # Django fixtures
│   ├── .env.example          # Environment variable template
│   ├── manage.py
│   ├── pyproject.toml
│   └── uv.lock
│
├── LICENSE
└── README.md
~~~

## 🚀 Running locally

Clone the repository:

~~~bash
git clone https://github.com/Giorgi61/django-test-DEVSPACE.git
cd django-test-DEVSPACE/DevSpace
~~~

Install dependencies with uv:

~~~bash
uv sync
~~~

Configure the environment variables using the provided .env.example:

~~~bash
cp .env.example .env
~~~

Open .env and provide the required values for your local PostgreSQL database and external services.

Then apply migrations:

~~~bash
uv run python manage.py migrate
~~~

Create an administrator:

~~~bash
uv run python manage.py createsuperuser
~~~

Run the development server:

~~~bash
uv run python manage.py runserver
~~~

The development server will normally be available at:

~~~text
http://127.0.0.1:8000/
~~~

## ⚙️ Configuration

The project uses **python-dotenv** to load configuration from a local .env file. Django settings read values such as the secret key, database credentials, OAuth credentials, email settings, and Cloudflare Turnstile credentials from environment variables instead of storing them directly in settings.py.

A template with the required variables is provided here:

~~~text
DevSpace/.env.example
~~~

Copy it to .env and fill in the values required for your local setup:

~~~bash
cp .env.example .env
~~~

The .env file is intended for local use and should **never be committed to Git**. Only .env.example, containing empty or non-sensitive placeholder values, belongs in the repository.

The project currently integrates several external services:

- PostgreSQL
- Google OAuth2
- SMTP email
- Cloudflare Turnstile

## 📌 Project Notes

This repository represents a stage of my Django learning process rather than a finished application.

The code contains experiments, refactors, and decisions made while learning the framework. Some parts are intentionally simple, while others were written to explore how Django's internals and extension points work.

The project should therefore be viewed primarily as a **learning sandbox**.

## 📄 License

This project is licensed under the **GNU General Public License v3.0**.

See [LICENSE](./LICENSE) for details.
