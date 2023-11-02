# Instructions

Web app: https://github.com/minhn4/webapp

## Postgres setup

Pull and run:

`docker pull postgres:16-alpine`

`export POSTGRES_DB=<YOUR_POSTGRES_DB_NAME> POSTGRES_USER=<YOUR_POSTGRES_USER> POSTGRES_PASSWORD=<YOUR_POSTGRES_PASSWORD>`

`docker run --name backend-postgres -e POSTGRES_DB=${POSTGRES_DB} -e POSTGRES_USER=${POSTGRES_USER} -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD}  -p 5432:5432 -d postgres:16-alpine`

Stop and restart:

`docker stop backend-postgres`

`docker restart backend-postgres`

psql

`psql -h localhost -p 5432 -U <YOUR_POSTGRES_USER> -d <YOUR_POSTGRES_DB_NAME> -c '\dt'`

## Virtual environment

Create and activate a venv:

`python3 -m venv venv`

`source venv/bin/activate`

Django setup:

`pip3 install -r requirements.txt`

`python3 manage.py migrate`

Deactivate venv:

`deactivate`

## Init

`pip3 install Django django-environ "psycopg[binary]" hvac cython python-minifier`

`pip3 freeze > requirements.txt`

## Standalone run

### Compile Python to binary (shared object)

This Python script minifies all `.py` files and compiles them to binary files (`.so`) recursively.

All `.c` and compiled `.py` files will be deleted automatically upon compilation.

Run:

`pip3 install cython python-minifier`

`python3 compile_to_binary.py build_ext --inplace`

### Migrate secrets to Vault

This Python script migrates all env vars from `.env` file to Vault.

This file contains Vault root token as raw text; DELETE this file after you are done.

Run:

`pip3 install hvac`

`python3 migrate_to_vault.py`
