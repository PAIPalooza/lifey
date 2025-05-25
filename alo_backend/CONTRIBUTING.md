# Contributing to ALO Backend

Thank you for your interest in contributing to the Automated Life Organizer (ALO) Backend! We appreciate your time and effort in helping us improve this project.

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** to your local machine:
   ```bash
   git clone https://github.com/your-username/lifey.git
   cd lifey/alo_backend
   ```
3. **Set up the development environment** (see [Development Setup](#development-setup) below).
4. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
5. **Make your changes** and commit them with a clear and descriptive message.
6. **Push your changes** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a pull request** against the `main` branch of the upstream repository.

## Development Setup

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Git

### Environment Setup

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Update the `.env` file with your configuration.

4. **Start the development environment**:
   ```bash
   ./run_dev.sh
   ```
   This will start all necessary services, run migrations, and initialize the database with test data.

## Development Workflow

### Running Tests

```bash
make test
```

### Linting and Formatting

```bash
# Run linters
make lint

# Format code
make format

# Check code formatting
make check-format

# Run type checking
make check-types
```

### Database Migrations

1. **Create a new migration**:
   ```bash
   alembic revision --autogenerate -m "Your migration message"
   ```

2. **Apply migrations**:
   ```bash
   alembic upgrade head
   ```

### API Documentation

The API documentation is automatically generated using OpenAPI and can be accessed at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
- Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for documentation.
- Keep lines under 88 characters (Black's default).
- Type hints are required for all function signatures and public APIs.

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Example:

```
feat(auth): add user registration endpoint

- Add POST /auth/register endpoint
- Add input validation with Pydantic
- Add tests for user registration

Closes #123
```

## Pull Requests

- Keep pull requests focused on a single feature or bug fix.
- Update documentation and tests as needed.
- Ensure all tests pass before submitting a pull request.
- Reference any related issues in the pull request description.

## Code Review

- All pull requests require at least one approval before merging.
- Be respectful and constructive in code reviews.
- Address all feedback before merging.

## Reporting Issues

When reporting issues, please include:

1. A clear and descriptive title.
2. Steps to reproduce the issue.
3. Expected behavior.
4. Actual behavior.
5. Any relevant logs or screenshots.
6. Your environment (OS, Python version, etc.).

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
