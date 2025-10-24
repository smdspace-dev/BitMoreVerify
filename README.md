# 🛡️ BitMoreVerify

<p align="center">
  <img src="https://img.shields.io/badge/Django-5.2.5-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
  <img src="https://img.shields.io/github/issues/smdspace-dev/BitMoreVerify?style=for-the-badge&color=blue" />
  <img src="https://img.shields.io/github/stars/smdspace-dev/BitMoreVerify?style=for-the-badge&color=gold" />
</p>

A full-stack authentication system built with **Django REST Framework** and **React**, featuring **Google OAuth**, **email verification**, and **News API** integration. Perfect for rapid development of secure authentication systems.

---

## ✨ Features

* **User Authentication**

  * Email/password registration and login
  * Google OAuth 2.0 integration
  * JWT token-based authentication
  * Email verification with OTP
  * Password reset functionality

* **Security Features**

  * Secure password hashing
  * CORS configuration
  * JWT token management
  * Environment-based configuration

* **News Integration**

  * News API integration for content delivery
  * Carousel display components
  * Real-time news updates

* **Modern UI/UX**

  * Responsive React frontend
  * Material design components
  * Weather information display
  * Professional landing page

---

## 🛠️ Tech Stack

### Backend

* **Django 5.2.5** - Web framework
* **Django REST Framework** - API development
* **PostgreSQL** - Database
* **JWT Authentication** - Token-based auth
* **Google OAuth** - Social authentication
* **Django Allauth** - Authentication package

### Frontend

* **React** - UI library
* **Create React App** - Build tool
* **Google OAuth** - Social login
* **CSS3** - Styling

---

## 📁 Project Structure

```
BitMoreVerify/
├── backend/                 # Django backend
│   ├── backend/            # Main Django settings
│   ├── users/              # User authentication app
│   ├── news/               # News API integration
│   ├── manage.py
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── styles/         # CSS files
│   │   └── utils/          # Utility functions
│   ├── public/
│   └── package.json
└── README.md
```

---

## 🚀 Quick Start

### 🧩 Prerequisites

* Python 3.8+
* Node.js 14+
* PostgreSQL 12+
* Git

### 1️⃣ Clone Repository

```bash
git clone https://github.com/smdspace-dev/BitMoreVerify.git
cd BitMoreVerify
```

### 2️⃣ Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Update with your values
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 3️⃣ Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env  # Update with your values
npm start
```

---

## ⚙️ Configuration

### Backend `.env`

```env
DJANGO_SECRET_KEY=your-django-secret-key
DEBUG=True

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

NEWSDATA_API_KEY=your-newsdata-api-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### Frontend `.env`

```env
REACT_APP_API_BASE_URL=http://127.0.0.1:8000
REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id
```

---

## 📚 API Documentation

| Method | Endpoint                     | Description         |
| ------ | ---------------------------- | ------------------- |
| POST   | `/api/auth/register/`        | User registration   |
| POST   | `/api/auth/login/`           | User login          |
| POST   | `/api/auth/logout/`          | Logout              |
| POST   | `/api/auth/verify-otp/`      | Email verification  |
| POST   | `/api/auth/forgot-password/` | Password reset      |
| POST   | `/api/auth/google/`          | Google OAuth login  |
| GET    | `/api/auth/user/`            | Get user profile    |
| PUT    | `/api/auth/user/`            | Update user profile |
| DELETE | `/api/auth/user/`            | Delete user account |

---

## 🧪 Development

### Run Tests

```bash
cd backend && python manage.py test
cd ../frontend && npm test
```

### Code Style

```bash
# Backend
black . && flake8 .

# Frontend
npm run lint
```

### Development Workflow

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make and test changes locally
3. Commit: `git commit -m "Add new feature"`
4. Push: `git push origin feature/new-feature`
5. Open Pull Request

---

## 🚀 Deployment

### Backend (Heroku)

```bash
heroku create bitmoreverify
heroku config:set DEBUG=False DJANGO_SECRET_KEY=your-production-secret
heroku config:set DATABASE_URL=your-prod-db-url
heroku run python manage.py migrate
git push heroku main
```

### Frontend (Netlify)

```bash
npm run build
# Upload build folder to Netlify or connect via Git
```

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add some AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 💬 Support

* 📧 Email: [ahilxdesigns@gmail.com](mailto:ahilxdesigns@gmail.com)
* 🐛 Issues: [GitHub Issues](https://github.com/smdspace-dev/BitMoreVerify/issues)

---

**Made with ❤️ by [Smd-space](https://github.com/smdspace-dev) and Team**
*Happy Coding! 🚀*
