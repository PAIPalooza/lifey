.PHONY: help install test lint format check-format check-types check-deps clean

# Help target to show all available commands
help:
	@echo "Available commands:"
	@echo "  make install     - Install development dependencies"
	@echo "  make test        - Run tests with coverage"
	@echo "  make lint        - Run linters"
	@echo "  make format      - Format code with black and isort"
	@echo "  make check-format - Check code formatting"
	@echo "  make check-types - Run type checking with mypy"
	@echo "  make check-deps   - Check for outdated dependencies"
	@echo "  make clean       - Clean up temporary files"

# Install development dependencies
install:
	pip install -e ".[dev]"

# Run tests with coverage
test:
	pytest tests/ -v --cov=app --cov-report=term-missing

# Run linters
lint:
	flake8 app tests
	mypy app tests

# Format code with black and isort
format:
	black app tests
	isort app tests

# Check code formatting
check-format:
	black --check app tests
	isort --check-only app tests

# Run type checking with mypy
check-types:
	mypy app tests

# Check for outdated dependencies
check-deps:
	pip list --outdated

# Clean up temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -r {} +
