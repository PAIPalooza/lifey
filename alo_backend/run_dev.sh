#!/bin/bash

# Exit on error
set -e

# Start the development environment
echo "Starting development environment..."
docker-compose up --build -d

# Wait for the database to be ready
echo "Waiting for database to be ready..."
until docker-compose exec -T db pg_isready -U postgres > /dev/null; do
  sleep 1
done

# Run database migrations
echo "Running database migrations..."
docker-compose exec web ./migrate.sh

# Initialize the database with test data
echo "Initializing database with test data..."
docker-compose exec web ./init_db.sh

echo ""
echo "Development environment is now running!"
echo "- API: http://localhost:8000"
echo "- API Docs: http://localhost:8000/docs"
echo "- pgAdmin: http://localhost:5050 (email: admin@alo.com, password: admin)"
