#!/bin/bash

sudo apt-get update -y
sudo apt-get install -y docker.io
sudo usermod -aG docker $USER
sudo apt-get install -y docker-compose

echo "Logging in to Docker Hub..."
docker login --username anikjobdesk --password-stdin <<< "Anik@2200"

echo "Docker setup and login complete!"
