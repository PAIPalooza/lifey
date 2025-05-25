#!/bin/bash

# Exit on error
set -e

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

echo "Migrations completed successfully!"
