# Contacts Management API

A production-ready RESTful API for managing contacts with JWT authentication, email verification, and cloud storage integration. Built with FastAPI and PostgreSQL.

## Features

- **🔐 JWT Authentication** - Secure user registration and login with refresh tokens
- **📧 Email Verification** - Token-based email verification system
- **🔄 Refresh Tokens** - Long-lived sessions with automatic token rotation
- **🖼️ Avatar Upload** - Profile picture upload with Cloudinary CDN integration
- **🌐 CORS Enabled** - Cross-Origin Resource Sharing support for frontend integration
- **🚦 Rate Limiting** - API abuse protection (10 requests/min on sensitive endpoints)
- **👤 User Isolation** - Each user can only access their own contacts
- **🔒 Password Security** - Bcrypt password hashing
- **📊 Full CRUD Operations** - Create, Read, Update, Delete contacts
- **🔍 Advanced Search** - Search contacts by name, email, or phone
- **🎂 Birthday Tracking** - Find contacts with upcoming birthdays
- **✅ Data Validation** - Pydantic schemas with type validation
- **📄 Pagination** - Efficient data retrieval with limit/offset
- **🏗️ Clean Architecture** - N-layer architecture with repositories and services
- **📚 API Documentation** - Interactive Swagger/OpenAPI documentation
- **🐳 Docker Support** - Complete containerization with Docker Compose

## Technology Stack

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migration tool
- **JWT** - JSON Web Tokens for authentication
- **Cloudinary** - Cloud-based image storage and optimization
- **Docker** - Containerization and deployment
- **MailHog** - Email testing in development

## Quick Start

### Docker Deployment (Recommended)

Run the entire stack with one command:

```bash
# 1. Configure environment variables
cp .env.docker.example .env
# Edit .env and add your Cloudinary credentials

# 2. Start all services (API, Database, MailHog)
docker-compose up -d --build

# 3. Access the API
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# MailHog: http://localhost:8025
```

The Docker setup includes:
- **FastAPI application** with auto-migration on startup
- **PostgreSQL database** with persistent storage
- **MailHog** for email testing

### Local Development

For local development without Docker:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment (.env file)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/contacts_db
SECRET_KEY=your-secret-key-here
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# 3. Start PostgreSQL database
docker-compose up -d db

# 4. Run database migrations
alembic upgrade head

# 5. Start the application
python main.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 6. Access the API
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

For email testing in local development, start MailHog:
```bash
docker-compose up -d mailhog
# View emails at: http://localhost:8025
```
## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/contacts_db

# JWT Authentication
SECRET_KEY=your-secret-key-min-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email Configuration
MAIL_USERNAME=test@example.com
MAIL_PASSWORD=
MAIL_FROM=noreply@contactsapi.com
MAIL_PORT=1025
MAIL_SERVER=localhost
MAIL_FROM_NAME=Contacts API

# Cloudinary (for avatar uploads)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

### Getting Cloudinary Credentials

1. Sign up at [cloudinary.com](https://cloudinary.com) (free tier available)
2. Get your credentials from the dashboard:
   - Cloud Name
   - API Key
   - API Secret
3. Add them to your `.env` file

## Authentication

All contact operations require JWT authentication.

### Authentication Flow

**1. Register a new user:**
```bash
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**2. Verify email:**
- Check your email (or MailHog at http://localhost:8025)
- Click verification link or use: `GET /auth/verify-email/{token}`

**3. Login to get tokens:**
```bash
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepass123
```

Response:
```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

**4. Use access token for API requests:**
```bash
GET /contacts/
Authorization: Bearer <access_token>
```

**5. Refresh expired tokens:**
```bash
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "<refresh_token>"
}
```

**Token Information:**
- **Access Token**: Valid for 30 minutes - use for API calls
- **Refresh Token**: Valid for 7 days - use to get new access tokens
- Refresh tokens are stored in database and can be revoked
- Token rotation: old refresh token is invalidated when new one is issued

## API Endpoints

### Authentication Endpoints
| Method | Endpoint | Description | Auth Required | Rate Limit |
|--------|----------|-------------|---------------|------------|
| POST | `/auth/register` | Register new user & send verification email | No | - |
| GET | `/auth/verify-email/{token}` | Verify email address | No | - |
| POST | `/auth/resend-verification` | Resend verification email | No | - |
| POST | `/auth/login` | Login and get access + refresh tokens | No | - |
| POST | `/auth/refresh` | Get new tokens using refresh token | No | - |
| POST | `/auth/logout` | Revoke refresh token (logout) | Yes | - |
| GET | `/auth/me` | Get current user profile | Yes | **10/min** |
| PATCH | `/auth/avatar` | Upload/update user avatar (Cloudinary) | Yes | - |

### Contact Endpoints (Protected - Require Authentication)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/contacts/` | Create new contact (returns 201) |
| GET | `/contacts/` | Get all contacts (paginated) |
| GET | `/contacts/search` | Search contacts |
| GET | `/contacts/birthdays` | Upcoming birthdays |
| GET | `/contacts/{id}` | Get contact by ID |
| PUT | `/contacts/{id}` | Update contact |
| DELETE | `/contacts/{id}` | Delete contact |

**Note:** All contact endpoints require `Authorization: Bearer <token>` header.

## Project Structure

```
goit-pythonweb-hw-10/
├── app/
│   ├── api/                    # API route handlers
│   │   ├── auth.py            # Authentication endpoints
│   │   └── contacts.py        # Contact management endpoints
│   ├── core/                   # Core configuration
│   │   ├── config.py          # Settings and environment variables
│   │   └── security.py        # JWT and password handling
│   ├── db/                     # Database configuration
│   │   └── database.py        # SQLAlchemy setup
│   ├── domain/                 # Database models
│   │   ├── base.py            # Base model class
│   │   ├── contact.py         # Contact model
│   │   ├── user.py            # User model
│   │   └── enums.py           # Enumerations
│   ├── repositories/           # Data access layer
│   │   ├── contact_repository.py
│   │   └── user_repository.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── contact.py         # Contact validation
│   │   └── user.py            # User validation
│   └── services/               # Business logic layer
│       ├── contact_service.py
│       ├── user_service.py
│       ├── email_service.py
│       └── cloudinary_service.py
├── alembic/                    # Database migrations
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Multi-container setup
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
└── .env                        # Environment variables
```

## API Documentation

**Interactive Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

The Swagger UI includes built-in authentication support - click "Authorize" to add your JWT token.

## Database Management

### Using Docker:
```bash
# View database logs
docker-compose logs db

# Access PostgreSQL shell
docker exec -it contacts_db psql -U postgres -d contacts_db

# View all tables
\dt

# Query users
SELECT email, is_confirmed FROM users;
```

### Migrations:
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

## Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f api

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# Remove everything including volumes
docker-compose down -v
```

## Testing

Access the API documentation at http://localhost:8000/docs to test all endpoints interactively.

### Example API Calls:

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Register User:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","first_name":"Test"}'
```

**Create Contact:**
```bash
curl -X POST http://localhost:8000/contacts/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john@example.com"}'
```


## License

This project is for educational purposes.

## Author

Created as part of GoIT Full Stack Web Development course.

