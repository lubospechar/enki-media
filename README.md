# Web-Based Storage for File Exchange

## Description
This project is a simple web-based storage platform for file exchange. It allows users to upload, share, and download files securely. The application is built using the Django framework, ensuring scalability, flexibility, and ease of use.

---

## Features
- User authentication (registration, login, logout).
- Upload and download files.
- File sharing with unique links.
- Admin panel for managing files and users.

---

## Installation

### Prerequisites
- Python (>= 3.8)
- pip
- A database system (e.g., PostgreSQL, MySQL, SQLite)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/lubospechar/enki-media.git
   cd media
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/macOS
   # OR
   venv\Scripts\activate  # For Windows
   ```

3. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Migrate the database:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application at:
   ```
   http://127.0.0.1:8000
   ```

