import os
import hvac

# Authenticate with Vault
client = hvac.Client(url=os.environ["VAULT_ADDR"], token=os.environ["VAULT_TOKEN"])
if not client.is_authenticated():
    print("Vault authentication failed.")
    exit(1)

VAULT_MOUNT_POINT = "cmp-backend"
secrets = {}

try:
    # List all the secrets under the specified mount point
    response = client.secrets.kv.v2.list_secrets(mount_point=VAULT_MOUNT_POINT, path="")

    if response and response.get("data") and response["data"].get("keys"):
        secret_keys = response["data"]["keys"]
        for key in secret_keys:
            # Read the value of each secret
            secret = (
                client.secrets.kv.v2.read_secret_version(
                    mount_point=VAULT_MOUNT_POINT, path=key
                )["data"]["data"],
            )

            if secret:
                if secret[0][key] == '""':
                    secret[0][key] = ""
                secrets[key] = secret[0][key]
            else:
                print(f"Unable to read secret '{key}'.")
    else:
        print(f"No secrets found in '{VAULT_MOUNT_POINT}'.")
except hvac.exceptions.VaultError as e:
    print(f"Error listing or reading secrets in Vault: {e}")

print(secrets)
