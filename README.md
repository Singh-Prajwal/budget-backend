# Backend - Personal Budget Tracker API

This directory contains the Django and Django REST Framework (DRF) backend for the Personal Budget Tracker application. It provides a secure, token-based JSON API for all frontend operations.

## Features

*   **Custom User Model:** Uses `email` as the primary field for authentication.
*   **JWT Authentication:** Secure stateless authentication using `djangorestframework-simplejwt` with rotating refresh tokens for persistent sessions.
*   **User Registration:** A public endpoint for new user creation.
*   **CRUD Endpoints:** Full Create, Read, Update, Delete functionality for user-specific `Transactions`, `Categories`, and `Budgets`.
*   **Custom Summary Endpoint:** An efficient endpoint (`/api/summary/`) that aggregates all necessary data for the main dashboard in a single API call.
*   **Filtering and Search:** The transactions endpoint supports filtering by type (income/expense) and searching by description or category.


### TEST USER Credentials: 
TEST USER Credentials
Email: prajwal.singh.226@gmail.com    
Password: Lpassword@0

## API Endpoints

All endpoints are prefixed with `/api/` and require an `Authorization: Bearer <token>` header, except for the public registration and token endpoints.

| Method | Endpoint                    | Description                                       |
| ------ | --------------------------- | ------------------------------------------------- |
| `POST` | `/user/register/`           | **Public:** Create a new user account.            |
| `POST` | `/token/`                   | **Public:** Obtain JWT access and refresh tokens. |
| `POST` | `/token/refresh/`           | **Public:** Refresh an expired access token.      |
| `GET`, `POST` | `/categories/`       | List all or create a new category for the user.   |
| `GET`, `POST` | `/transactions/`     | List all (paginated/filtered) or create a new transaction. |
| `GET`, `PUT`, `DELETE` | `/transactions/{id}/` | Retrieve, update, or delete a single transaction. |
| `POST` | `/budgets/`                 | Create or update budgets for one or more categories (bulk-friendly). |
| `GET`  | `/summary/`                 | Get a full financial summary for the dashboard.   |


## Local Setup

1.  Ensure you are in the `backend` directory.
2.  Create a Python virtual environment: `python -m venv venv`
3.  Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4.  Install dependencies: `pip install -r requirements.txt`
5.  Apply database migrations: `python manage.py migrate`
6.  Create a superuser for admin access: `python manage.py createsuperuser`
7.  Run the development server: `python manage.py runserver`

The API will be available at `http://127.0.0.1:8000/api/`.