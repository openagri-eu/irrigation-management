#!/bin/bash

# Exit script on error
set -e


# Check whether these values have been passed
if [ -z "${POSTGRES_USER}" ]; then
  echo "Postgres username is not set in env"
  exit
fi

if [ -z "${POSTGRES_PASSWORD}" ]; then
  echo "Postgres password is not set in env"
  exit
fi

if [ -z "${POSTGRES_HOST}" ]; then
  echo "Postgres hostname is not set in env"
  exit
fi

if [ -z "${POSTGRES_PORT}" ]; then
  echo "Postgres port is not set in env"
  exit
fi

if [ -z "${POSTGRES_DB}" ]; then
  echo "Postgres database name is not set in env"
  exit
fi

# Before the migrations can take place, we need to build the connection string in the alembic.ini file
sed -i -e "s/PGU/${POSTGRES_USER}/g" -e "s/PGP/${POSTGRES_PASSWORD}/g" -e "s/PGH/${POSTGRES_HOST}/g" -e "s/PGO/${POSTGRES_PORT}/g" -e "s/PGD/${POSTGRES_DB}/g" ./alembic.ini


# Migrate sqlalchemy models to postgres via alembic
echo "Starting db migrations"

alembic upgrade head
#exit_code=$?
#count=0
#
#while [[ "${exit_code}" -ne 0 && "${count}" -lt 5 ]]
#do
#  count=$((count+1))
#  echo "${count}"
#
#  alembic upgrade head
#
#  exit_code=$?
#  sleep 2
#done

echo "Finished db migrations"


# Start the FastAPI app with uvicorn
echo "Starting Uvicorn server"

exec uvicorn --host 0.0.0.0 --port 80 --app-dir=app 'main:app'

echo "Started Uvicorn server"
