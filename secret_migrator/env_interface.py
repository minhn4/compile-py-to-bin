from pathlib import Path
import hvac
import environ

# Authenticate with Vault
client = hvac.Client(url="http://localhost:8300/", token="hvs.Y30WrR6bAp7vtpaVBQlueAcn")
if not client.is_authenticated():
    print("Vault authentication failed, using .env file instead")
    exit(1)

    # BASE_DIR = Path(__file__).resolve().parent

    # env = environ.Env()
    # env.read_env(BASE_DIR / ".env")

else:
    VAULT_MOUNT_POINT = "cmp-backend"
    secrets = {}

    try:
        # List all the secrets under the specified mount point
        response = client.secrets.kv.v2.list_secrets(
            mount_point=VAULT_MOUNT_POINT, path=""
        )

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

    def env(key, val_type, val):
        if type(val) != val_type:
            print("error: type mismatch")
            exit(1)

        if val_type == str:
            return secrets[key] if secrets[key] else val
        if val_type == bool:
            return True if secrets[key] else False
        return int(secrets[key]) if secrets[key] else val


print(env("EMAIL_USE_FILE_BACKEND", bool, False))
print(env("EMAIL_HOST", str, "localhost"))
print(env("EMAIL_PORT", int, 465))
