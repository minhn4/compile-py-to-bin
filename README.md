# Instructions

## Compile Python to binary (shared object)

This Python script minifies all `.py` files and compiles them to binary files (`.so`) recursively.

All `.c` and compiled `.py` files will be deleted automatically upon compilation.

Run:

`pip3 install cython python-minifier`

`python3 compile_to_binary.py build_ext --inplace`

## Migrate secrets to Vault

This Python script migrates all env vars from `.env` file to Vault.

This file contains Vault root token as raw text; DELETE this file after you are done.

Run:

`pip3 install hvac`

`python3 migrate_to_vault.py`
