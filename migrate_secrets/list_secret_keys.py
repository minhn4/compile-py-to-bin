import os
import hvac

# Authenticate with Vault
client = hvac.Client(
    url=os.environ["VAULT_ADDR"], token=os.environ["VAULT_TOKEN"])
if not client.is_authenticated():
    print("Vault authentication failed.")
    exit(1)

vault_mount_point = "cmp-backend"

try:
    # List all the secrets under the specified mount point
    response = client.secrets.kv.v2.list_secrets(
        mount_point=vault_mount_point, path="")

    print(response)

    if response and response.get('data') and response['data'].get('keys'):
        secrets = response['data']
        print(type(secrets))
        # print(f"Secrets in '{vault_mount_point}':")
        # for secret in secrets:
        #     print(secret)
    else:
        print(f"No secrets found in '{vault_mount_point}'.")
except hvac.exceptions.VaultError as e:
    print(f"Error listing secrets in Vault: {e}")
