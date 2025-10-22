# BitMoreVerify 🚀

A full-stack authentication system built with Django REST Framework and React, featuring Google OAuth integration, email verification, and news API integration. Perfect for rapid development of secure authentication systems.

## ✨ Features

- **User Authentication**
  - Email/password registration and login
  - Google OAuth 2.0 integration
  - JWT token-based authentication
  - Email verification with OTP
  - Password reset functionality

- **Security Features**
  - Secure password hashing
  - CORS configuration
  - JWT token management
  - Environment-based configuration

- **News Integration**
  - News API integration for content delivery
  - Carousel display components
  - Real-time news updates

- **Modern UI/UX**
  - Responsive React frontend
  - Material design components
  - Weather information display
  - Professional landing page

## 🛠️ Tech Stack

### Backend
- **Django 5.2.5** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database
- **JWT Authentication** - Token-based auth
- **Google OAuth** - Social authentication
- **Django Allauth** - Authentication package

### Frontend
- **React** - UI library
- **Create React App** - Build tool
- **Google OAuth** - Social login
- **CSS3** - Styling

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

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- Git

### 1. Clone Repository

```bash
git clone https://github.com/your-username/BitMoreVerify.git
cd BitMoreVerify
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux  
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your actual values

# Database setup
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env
# Edit .env with your actual values

# Start development server
npm start
```

## ⚙️ Configuration

### Environment Variables

#### Backend (.env)
```env
# Django Configuration
DJANGO_SECRET_KEY=your-django-secret-key
DEBUG=True

# Database Configuration
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# API Keys
NEWSDATA_API_KEY=your-newsdata-api-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

#### Frontend (.env)
```env
REACT_APP_API_BASE_URL=http://127.0.0.1:8000
REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id
```

### Required API Keys

1. **Google OAuth Credentials**
   - Go to [Google Cloud Console](https://console.developers.google.com/)
   - Create a new project or select existing
   - Enable Google+ API
   - Create OAuth 2.0 credentials
   - Add authorized redirect URIs

2. **News API Key**
   - Visit [NewsData.io](https://newsdata.io/)
   - Sign up for a free account
   - Get your API key from dashboard

3. **Email Configuration**
   - For Gmail: Enable 2-factor authentication
   - Generate App Password: [Gmail App Passwords](https://support.google.com/accounts/answer/185833)

### Database Setup

#### PostgreSQL Installation
```bash
# Install PostgreSQL
# Windows: Download from postgresql.org
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql

# Create database and user
sudo -u postgres psql
CREATE DATABASE your_database_name;
CREATE USER your_database_user WITH PASSWORD 'your_database_password';
GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_database_user;
\\q
```

#### Alternative: SQLite (Development)
Uncomment SQLite configuration in `settings.py` for simpler development setup.

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | User registration |
| POST | `/api/auth/login/` | User login |
| POST | `/api/auth/logout/` | User logout |
| POST | `/api/auth/verify-otp/` | Email verification |
| POST | `/api/auth/forgot-password/` | Password reset |
| POST | `/api/auth/google/` | Google OAuth login |

### User Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/auth/user/` | Get user profile |
| PUT | `/api/auth/user/` | Update user profile |
| DELETE | `/api/auth/user/` | Delete user account |

### Example Requests

#### User Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

#### User Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

## 🔧 Development

### Running Tests
```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

### Code Style
```bash
# Backend formatting
black .
flake8 .

# Frontend formatting
npm run lint
```

### Development Workflow
1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes and test locally
3. Commit changes: `git commit -m "Add new feature"`
4. Push branch: `git push origin feature/new-feature`
5. Create pull request

## 🚀 Deployment

### Backend Deployment (Heroku)
```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn backend.wsgi" > Procfile

# Create requirements.txt
pip freeze > requirements.txt

# Deploy
heroku create your-app-name
heroku config:set DEBUG=False
heroku config:set DJANGO_SECRET_KEY=your-production-secret
# Set other environment variables
git push heroku main
heroku run python manage.py migrate
```

### Frontend Deployment (Netlify)
```bash
# Build for production
npm run build

# Deploy to Netlify
# Upload build folder or connect Git repository
```

## 📝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- 📧 Email: support@bitmore.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/BitMoreVerify/issues)
- 📖 Documentation: [Wiki](https://github.com/your-username/BitMoreVerify/wiki)

## 🙏 Acknowledgments

- Django REST Framework team
- React team
- Google OAuth team
- NewsData.io for news API
- All contributors and supporters

---

**Made with ❤️ by the BitMore Team**

*Happy Coding! 🚀*