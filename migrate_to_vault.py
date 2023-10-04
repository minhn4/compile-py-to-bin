'''
Author: Minh Nguyen
Date: Oct 2023

This Python script migrates all env vars from .env file to Vault.
This file contains Vault root token as raw text; DELETE this file after you are done.

Run:
pip3 install hvac
python3 migrate_to_vault.py
'''

import os
import hvac

# Load environment variables from .env file
env_file_path = ".env"

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
    env_vars[key] = value

# Authenticate with Vault
vault_url = "http://127.0.0.1:8200"  # Replace with your Vault URL
vault_token = "hvs.LBdO5lFquLh9VEhu8E75KFFc"  # Replace with your Vault token

client = hvac.Client(url=vault_url, token=vault_token)

if not client.is_authenticated():
    print("Vault authentication failed.")
    exit(1)

# Write environment variables to Vault's secret storage
vault_secret_path = "cmp-backend"  # Replace with your desired path in Vault

for key, value in env_vars.items():
    client.secrets.kv.v2.create_or_update_secret(
        path=vault_secret_path,
        secret=key,
        data={"value": value}
    )
    print(f"Variable '{key}' written to Vault.")

print("Environment variables have been successfully moved to Vault.")
