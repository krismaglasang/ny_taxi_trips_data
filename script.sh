#! /bin/sh

docker build -t ingestion_script:0.01 ./
docker compose up -d
