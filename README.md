# Instructions

Web app: https://github.com/minhn4/webapp

## Init

`pip3 install Django django-environ "psycopg[binary]" hvac cython python-minifier`

`pip3 freeze > requirements.txt`

## Postgres setup

`pip3 install "psycopg[binary]"`

`docker pull postgres:16-alpine`

`docker run --name backend-postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -p 5432:5432 -d postgres:16-alpine`

`docker restart backend-postgres`

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
