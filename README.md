# movie_management_platform_backend

## Table of Contents

* [Overview](#overview)
* [Key Features](#key-features)
* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
    * [Configuration](#configuration)
    * [Running the Development Server](#running-the-development-server)
* [Usage](#usage)
    * [API Endpoints](#api-endpoints)

## Getting Started

### Prerequisites

Make sure you have the following installed:

* **Python:** Version 3.8 or higher. You can download it from [python.org](https://www.python.org/downloads/).
* **pip:** Python package installer (usually comes with Python).
* **Virtualenv or venv:** For creating isolated Python environments.

### Installation

1.  **Clone the repository (if applicable):**

    ```bash
    git clone https://github.com/densentsu124/movie_management_platform_backend.git
    cd movie_management_platform_backend
    ```

2.  **Create a virtual environment:**

    ```bash
    # Using virtualenv
    virtualenv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows

    # Or using venv (built-in to Python 3)
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

3.  **Install the project dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  **Run migrations:**

    ```bash
    python manage.py migrate
    ```

2.  **Create a superuser (for accessing the admin interface):**

    ```bash
    python manage.py createsuperuser
    ```


### Running the development server

1. ```bash
    python manage.py runserver
    ```

# USAGE

## Authentication

*Simple REST JWT*

* **Bearer Token (JWT):** Include an access token in the `Authorization` header (e.g., `Authorization: Bearer your_access_token`).

To gain access and refresh tokens, access the following API endpoints:

* `/api/token/`
* **Request Body:**
    ```json
    {
        "username":"<username>",
        "password":"<password>"
    }
    ```
* **Response Body:**
    ```json
    {
        "access":"<access_token>",
        "refresh":"<refresh_token>"
    }
    ```
* `/api/token/refresh`
* **Request Body:**
    ```json
    {
        "refresh":"<refresh_token>"
    }
    ```
* **Response Body:**
    ```json
    {
        "access":"<access_token>"
    }
    ```

### api-endpoints

    The API endpoints are available under `/movies/`

**Common Request Headers:**
    `[Authorization]`: Bearer [Contains the JWT Token] (Required)

*`/movies/`*
* **METHOD: GET**
* **Response Body:**
    ```json
    {
        [
            "title":<STRING>,
            "description":<STRING>,
            "date_added":<DATETIME>,
            "video_file":<STRING>, // File path of the video file in the machine
            "thumbnail" :<STRING> // File path of the thumbnail file in the machine
        ]
    }
    ```

* **METHOD: POST**
* **Request Body**
    ``` form-data
    {
        "video_name":<string>, // Title
        "video_file":<file>, // Video file
        "description":<string>, //Description
    }
    ```
* **Response Body:**
    ```json
    {
        "title":<STRING>,
        "description":<STRING>,
        "date_added":<DATETIME>,
        "video_file":<STRING>, // File path of the video file in the machine
        "thumbnail" :<STRING> // File path of the thumbnail file in the machine
    }
    ```


*`/movies/<int:id>`*
* **METHOD: GET**
* **Response Body:**
    ```json
    {
        "title":<STRING>,
        "description":<STRING>,
        "date_added":<DATETIME>,
        "video_file":<STRING>, // File path of the video file in the machine
        "thumbnail" :<STRING> // File path of the thumbnail file in the machine
    }
    ```

* **METHOD: PUT**
* **Response Body:**
    ```json
    {
        "title":<STRING>,
        "description":<STRING>,
        "date_added":<DATETIME>,
        "video_file":<STRING>, // File path of the video file in the machine
        "thumbnail" :<STRING> // File path of the thumbnail file in the machine
    }
    ```

*`/movies/video/<int:id>`*
* **METHOD: GET**
* **Response Body:**
    ```json
        "No response body"
    ```

*`/movies/thumbnail/<int:id>`*
* **METHOD: GET**
* **Response Body:**
    ```json
        "No response body"
    ```
