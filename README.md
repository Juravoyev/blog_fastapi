# 📝 Blog Engine REST API (FastAPI & Alembic)

![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-4169E1?style=for-the-badge)
![Email Service](https://img.shields.io/badge/Email-SMTP_Service-EA4335?style=for-the-badge&logo=gmail&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A production-ready asynchronous RESTful API backend for blogging platforms built with **FastAPI**, **SQLAlchemy**, **Alembic**, **JWT Authentication**, and automated **Email Notifications**.

---

## 🌟 Key Features

- **✍️ Article & Post Management**: Full CRUD operations for blog posts, categories, and comments.
- **🔐 JWT Authentication & Security**: Password hashing, token generation, and protected admin routes.
- **📧 Email Service (`email_service.py`)**: Asynchronous email delivery for user verification and updates.
- **🗄 Alembic Version Control**: Automated database schema migrations.
- **🖼 Media File Uploads**: Image and asset uploading handler for post thumbnails.
- **🧪 Pytest Integration**: Unit and integration test suite (`tests/`).

---

## ⚙️ How to Run

1. **Clone & Setup:**
   ```bash
   git clone https://github.com/Juravoyev/blog_fastapi.git
   cd blog_fastapi
   
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Variables:**
   ```bash
   cp .env.example .env
   ```

3. **Run Alembic Migrations:**
   ```bash
   alembic upgrade head
   ```

4. **Launch Server:**
   ```bash
   uvicorn main:app --reload
   ```
   Open `http://127.0.0.1:8000/docs` for API documentation.

---

## 👨‍💻 Author

**Shams Juravoyev**  
- Telegram: [@Juravoyev](https://t.me/Juravoyev)  
- LinkedIn: [Shams Juravoyev](https://www.linkedin.com/in/shams-juravoyev-3017473ab/)  
- GitHub: [@Juravoyev](https://github.com/Juravoyev)  
