# ALO Backend

Automated Life Organizer (ALO) - Backend Service

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9+

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/PAIPalooza/lifey.git
   cd lifey/alo_backend
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Update the `.env` file with your configuration.

3. **Build and start the services**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - pgAdmin: http://localhost:5050 (email: admin@alo.com, password: admin)

## Project Structure

```
alo_backend/
├── app/
│   ├── api/                  # API routes
│   │   └── api_v1/           # API version 1
│   │       └── api.py        # API router
│   ├── core/                 # Core functionality
│   │   ├── config.py         # Configuration settings
│   │   └── database.py       # Database connection
│   ├── __init__.py
│   └── main.py               # FastAPI application
├── tests/                    # Test files
├── .env.example              # Example environment variables
├── .gitignore
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                # Docker configuration
└── requirements.txt          # Python dependencies
```

## Development

### Running Tests

```bash
docker-compose exec web pytest
```

### Database Migrations

1. Install Alembic:
   ```bash
   pip install alembic
   ```

2. Create a migration:
   ```bash
   alembic revision --autogenerate -m "Your migration message"
   ```

3. Apply migrations:
   ```bash
   alembic upgrade head
   ```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
