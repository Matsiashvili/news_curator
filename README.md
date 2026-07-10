# News Curator and Reading List

News Curator and Reading List is a Flask-based web application that allows users to discover news articles, personalize their news feed, save articles for later, organize saved articles into reading lists, add private notes and tags, and track reading activity through statistics.

The project was built as a final Flask assignment and demonstrates core backend development concepts including application factories, blueprints, authentication, sessions, database relationships, external API integration, REST API endpoints, CSRF protection, custom decorators, service classes, and Jinja template inheritance.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Main Features](#main-features)
- [Tech Stack](#tech-stack)
- [Project Requirements Covered](#project-requirements-covered)
- [Application Structure](#application-structure)
- [Database Design](#database-design)
- [REST API Endpoints](#rest-api-endpoints)
- [External API Integration](#external-api-integration)
- [Security Features](#security-features)
- [Setup Instructions](#setup-instructions)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Testing the Main Features](#testing-the-main-features)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Project Overview

The application helps users manage their news reading workflow.

Users can register, log in, browse news from NewsAPI, filter articles by category, country, source, or search query, and save articles into personal reading lists. Saved articles can be marked as read or unread, tagged with user-defined labels, and given private notes with a maximum length of 500 characters.

The app also includes a statistics page where users can see how many articles they saved this week, which tags they use most often, and which news source appears most frequently in their saved articles.

---

## Main Features

### Authentication

- User registration
- User login and logout
- Password hashing using Werkzeug
- Flask sessions for logged-in users
- Custom `@login_required` decorator for protected pages

### News Browsing

- Fetches live news from NewsAPI
- Browse news by category
- Browse news by country
- Filter by news source
- Search news using NewsAPI `/everything` endpoint
- Pagination with 15 articles per page
- News cards with title, source, description, image, and article link

### User Preferences

- Users can select preferred categories
- Users can choose a default country
- Preferences are saved in the database
- News feed uses the user's preferences when available

### Saved Articles

- Save articles for later
- Prevent duplicate saved articles
- View all saved articles
- Delete saved articles
- Mark articles as read or unread
- Opening an article from saved articles automatically marks it as read

### Reading Lists

- Create named reading lists
- Save articles into selected reading lists
- View all reading lists
- Open individual reading lists
- View articles saved inside a specific list

### Notes

- Add private notes to saved articles
- Notes are limited to 500 characters
- Edit saved notes
- Delete notes

### Tags

- Add user-defined tags to saved articles
- Reuse existing tags
- Remove tags from saved articles
- Tags are displayed on saved article cards

### Statistics

The statistics page shows:

- Total saved articles
- Articles saved this week
- Read articles
- Unread articles
- Top saved news source
- Favorite tags

### Error Handling

- Custom 404 page
- Custom 500 page

### REST API

The application includes JSON API endpoints under the `/api/` prefix for news, saved articles, and reading lists.

---

## Tech Stack

### Backend

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Werkzeug Security
- Requests
- python-dotenv

### Database

- SQLite
- SQLAlchemy ORM

### Frontend

- HTML
- CSS
- Bootstrap 5
- Jinja2 templates

### External Service

- NewsAPI

---

## Project Requirements Covered

This project covers the required Flask final project specifications.

| Requirement | Status |
|---|---|
| Python 3.x and Flask | Completed |
| Application factory using `create_app()` | Completed |
| Minimum 2 blueprints | Completed |
| Flask-SQLAlchemy with SQLite | Completed |
| Minimum 3 database tables | Completed |
| One-to-many database relationship | Completed |
| Werkzeug password hashing | Completed |
| Flask sessions | Completed |
| Custom `@login_required` decorator | Completed |
| Jinja2 `base.html` inheritance | Completed |
| Custom Jinja filter | Completed |
| Form validation and flash messages | Completed |
| CSRF protection | Completed |
| Minimum 2 service classes | Completed |
| Inheritance demonstration | Completed |
| REST API with `/api/` prefix | Completed |
| External API integration | Completed |
| Pagination | Completed |
| Text search | Completed |
| Filtering | Completed |
| Custom 404 and 500 pages | Completed |

---

## Application Structure

```text
news_curator/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── decorators.py
│   ├── errors.py
│   ├── extensions.py
│   ├── filters.py
│   ├── models.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   │
│   ├── main/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── news/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── services.py
│   │
│   ├── reading_lists/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── services.py
│   │
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   │
│   └── templates/
│       ├── base.html
│       ├── errors/
│       ├── main/
│       ├── auth/
│       ├── news/
│       └── reading_lists/
│
├── run.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example