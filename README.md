# Contacts Management API

RESTful API for managing contacts with CRUD operations, built with FastAPI and PostgreSQL.

## Features

- Full CRUD operations (Create, Read, Update, Delete)
- Search contacts by name or email
- Find contacts with upcoming birthdays
- Data validation with Pydantic
- Pagination support
- N-layer architecture
- Swagger/OpenAPI documentation
- PostgreSQL database with Alembic migrations

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start PostgreSQL Database

```bash
docker-compose up -d
```

This starts PostgreSQL on port 5432 with:
- Database: `contacts_db`
- Username: `postgres`
- Password: `postgres`

### 3. Apply Database Migrations

```bash
alembic upgrade head
```

### 4. Start the API Server

```bash
# Using startup script
./start.sh

# Or directly
uvicorn main:app --reload
```

### 5. Open API Documentation

Open http://localhost:8000/docs to see interactive Swagger documentation.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/contacts/` | Create new contact |
| GET | `/contacts/` | Get all contacts (paginated) |
| GET | `/contacts/search` | Search contacts |
| GET | `/contacts/birthdays` | Upcoming birthdays |
| GET | `/contacts/{id}` | Get contact by ID |
| PUT | `/contacts/{id}` | Update contact |
| DELETE | `/contacts/{id}` | Delete contact |

## 🧪 Quick API Test

```bash
# Create a contact
curl -X POST "http://localhost:8000/contacts/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone_number": "+1234567890",
    "date_of_birth": "1990-01-15"
  }'

# Get all contacts
curl "http://localhost:8000/contacts/"

# Search contacts
curl "http://localhost:8000/contacts/search?q=john"
```

Or use Swagger UI at http://localhost:8000/docs to test endpoints interactively.

## Project Structure

```
app/
├── api/              # API endpoints
│   └── contacts.py
├── services/         # Business logic
│   └── contact_service.py
├── repositories/     # Data access
│   └── contact_repository.py
├── schemas/          # Pydantic validation
│   └── contact.py
├── domain/           # SQLAlchemy models
│   ├── base.py
│   └── contact.py
├── core/             # Configuration
│   └── config.py
└── db/               # Database
    └── database.py
```

## Database Management

```bash
# Check status
docker-compose ps

# View logs
docker-compose logs db

# Stop database
docker-compose down

# Connect to database
docker exec -it contacts_db psql -U postgres -d contacts_db
```

## Configuration

Database connection is configured in `.env` file:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/contacts_db
```

## Stop Server

```bash
lsof -ti:8000 | xargs kill -9
```

