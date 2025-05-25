#!/bin/bash

# Exit on error
set -e

# Stop and remove all containers and volumes
echo "Stopping and removing containers..."
docker-compose down -v

# Remove all unused containers, networks, and images
echo "Cleaning up Docker resources..."
docker system prune -f

echo "Development environment has been reset."
