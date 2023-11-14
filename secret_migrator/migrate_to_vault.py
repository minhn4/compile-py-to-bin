"""
Author: Minh Nguyen
Date: Oct 2023

This Python script migrates all env vars from .env file to Vault.
This file might contain Vault root token as raw text; DELETE this file after you are done.

Export env vars:
export VAULT_TOKEN=<YOUR_VAULT_TOKEN> VAULT_ADDR=https://<YOUR_VAULT_ADDRESS>

Run:
pip3 install hvac
python3 migrate_to_vault.py

Unset env vars upon finish:
unset VAULT_TOKEN VAULT_ADDR
"""

import os
import hvac

# Load environment variables from .env file
env_file_path = "env"

if not os.path.exists(env_file_path):
    print(f"{env_file_path} does not exist.")
    exit(1)

with open(env_file_path, "r") as env_file:
    env_lines = env_file.readlines()

# Parse .env file and store variables in a dictionary
env_vars = {}
for line in env_lines:
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    key, value = line.split("=", 1)
    if value == '""':
        value = ""
    env_vars[key] = value

# Authenticate with Vault
client = hvac.Client(
    url=os.environ["VAULT_ADDR"], token=os.environ["VAULT_TOKEN"])
if not client.is_authenticated():
    print("Vault authentication failed.")
    exit(1)

VAULT_MOUNT_POINT = "cmp-backend"

# Write environment variables to Vault's secret storage
for key, value in env_vars.items():
    secret = {}
    secret[key] = value
    client.secrets.kv.v2.create_or_update_secret(
        mount_point=VAULT_MOUNT_POINT,
        path=key,
        secret=secret,
    )
    print(f"Variable '{key}' has been successfully moved to Vault")
