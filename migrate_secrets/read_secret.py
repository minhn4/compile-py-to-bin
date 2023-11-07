import os
import hvac

# Authenticate with Vault
client = hvac.Client(
    url=os.environ["VAULT_ADDR"], token=os.environ["VAULT_TOKEN"])
if not client.is_authenticated():
    print("Vault authentication failed.")
    exit(1)

vault_mount_point = "cmp-backend"

secret = client.secrets.kv.v2.read_secret_version(
    mount_point=vault_mount_point, path='DB_USER')
print(secret['data']['data']['DB_USER'])
