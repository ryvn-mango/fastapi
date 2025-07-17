# FastAPI Backend Template

A production-ready FastAPI backend template for modern web applications

## Features

- **FastAPI Framework**: High-performance REST API with automatic OpenAPI documentation
- **SQLAlchemy ORM**: Database integration with migration support via Alembic
- **Authentication**: JWT token authentication ready to use
- **OpenTelemetry**: Built-in observability with tracing and metrics
- **Docker Support**: Containerization for easy deployment
- **CORS Configuration**: Pre-configured Cross-Origin Resource Sharing
- **Testing**: Set up with pytest for unit and integration tests
- **Code Quality**: Black, isort, flake8, and mypy configuration

## Getting Started

### Prerequisites

- Python 3.12+
- pip or [uv](https://github.com/astral-sh/uv) (recommended)

### Installation

#### Using pip

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

#### Using uv (recommended)

```bash
# Install uv if not already installed
pip install uv

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
ENVIRONMENT=development
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-secret-key-here
```

### Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000 with OpenAPI documentation at http://localhost:8000/docs.

## API Endpoints

- `/api/v1/items` - Item management endpoints
- `/api/v1/generate` - Generation endpoints

## Development

### Install Development Dependencies

```bash
pip install -e ".[dev]"  # Or: uv pip install -e ".[dev]"
```

### Code Formatting and Linting

```bash
# Format code
black .
isort .

# Lint code
flake8
mypy .
```

### Running Tests

```bash
pytest
```

## Docker Deployment

Build and run the Docker container:

```bash
docker build -t fastapi-backend .
docker run -p 8000:8000 fastapi-backend
```

## Project Structure

```
app/
├── api/                  # API endpoints
│   └── v1/
│       └── endpoints/    # API route definitions
├── core/                 # Core application modules
├── crud/                 # Database CRUD operations
├── db/                   # Database setup and session
├── models/               # SQLAlchemy models
└── schemas/              # Pydantic schemas
```

## License

This project is licensed under the MIT License.
