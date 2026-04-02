#!/bin/zsh

# Stopping application
sudo docker compose -f docker-compose.yml down

# Removeing containers (just in case)
sudo docker rm horse_races_nginx
sudo docker rm horse_races_app
sudo docker rm horse_races_db

# Removeing images
sudo docker rmi nginx-image
sudo docker rmi app-image
sudo docker rmi postgres-image
