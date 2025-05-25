#!/bin/bash

# Exit on error
set -e

# Run the database initialization script
echo "Initializing database with test data..."
python -m app.init_db

echo "Database initialization completed successfully!"
