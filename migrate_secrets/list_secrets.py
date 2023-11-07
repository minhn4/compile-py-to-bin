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

    if response and response.get('data') and response['data'].get('keys'):
        secrets = response['data']['keys']
        print(f"Secrets in '{vault_mount_point}':")
        print(secrets)
        for secret in secrets:
            # Read the value of each secret
            secret_path = f"{vault_mount_point}/{secret}"
            secret_response = client.secrets.kv.v2.read_secret_version(
                secret_path)

            if secret_response and secret_response.get('data') and secret_response['data'].get('data'):
                secret_data = secret_response['data']['data']
                print(f"Secret '{secret}':")
                for key, value in secret_data.items():
                    print(f"  {key}: {value}")
            else:
                print(f"Unable to read secret '{secret}'.")
    else:
        print(f"No secrets found in '{vault_mount_point}'.")
except hvac.exceptions.VaultError as e:
    print(f"Error listing or reading secrets in Vault: {e}")
