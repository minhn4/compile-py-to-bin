import os
import hvac
from dotenv import dotenv_values, set_key

# Vault secret path
VAULT_MOUNT_POINT = "cmp-backend"  # Replace with your desired mount point

# Initialize the Vault client
client = hvac.Client(
    url=os.environ["VAULT_ADDR"], token=os.environ["VAULT_TOKEN"])

# Check if Vault is sealed
if client.is_sealed():
    print("Vault is sealed. Unseal it before proceeding.")
    exit(1)

# Read all secrets at the specified mount point
secrets = client.secrets.kv.v2.read_secret_version(path=VAULT_MOUNT_POINT, path="")

if not secrets:
    print(f"No secrets found at mount point: {VAULT_MOUNT_POINT}")
    exit(1)

# Load the existing .env file if it exists
if os.path.exists('.env'):
    env_data = dotenv_values('.env')
else:
    env_data = {}

# Add or update secrets in the .env file
for key, value in secrets['data']['data'].items():
    env_data[key] = value

# Write the updated .env file
with open('.env', 'w') as env_file:
    for key, value in env_data.items():
        set_key(env_file, key, value)

print("Secrets have been written to .env file.")
