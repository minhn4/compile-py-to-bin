from pathlib import Path
import hvac
import environ

try:
    # Authenticate with Vault
    client = hvac.Client(
        url="http://localhost:8300", token="hvs.oDiyRE4MbsD2QZlAw0gQfGSM"
    )
    client.is_authenticated()
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
                        mount_point=VAULT_MOUNT_POINT,
                        path=key,
                        raise_on_deleted_version=True,
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

    def env(key, val_type=None, val=None):
        if val_type != None and val == None:
            print("ImproperlyConfigured")
            return

        if key in secrets:
            if val_type == bool:
                if secrets[key].lower() == "false":
                    return False
                return True
            return secrets[key]

        return val

except Exception:
    print("Vault access failed, using .env file instead...")
    print()

    BASE_DIR = Path(__file__).resolve().parent

    env = environ.Env()
    env.read_env(BASE_DIR / ".env")


foo = env("EMAIL_USE_FILE_BACKEND", bool, False)
print(foo, type(foo))

# foo = env("EMAIL_HOST", str, "localhost")
# print(foo, type(foo))

# foo = env("EMAIL_PORT", int, 465)
# print(foo, type(foo))

# foo = env("EMAIL_PORT", int, True)
# print(foo, type(foo))

# foo = env("EMAIL_PORT", bool, "465")
# print(foo, type(foo))

# foo = env("EMAIL_PORT", str, 465)
# print(foo, type(foo))

# foo = env("xxx", bool, "True")
# print(foo, type(foo))
