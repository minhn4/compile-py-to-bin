from pathlib import Path
import hvac
import environ

BASE_DIR = Path(__file__).resolve().parent

try:
    # set mount point to 'cmp-backend' for Vault, set to '' to use .env instead
    VAULT_MOUNT_POINT = 'cmp-backend-local'
    VAULT_ADDR = 'http://10.240.201.233:8200'
    VAULT_TOKEN = 'hvs.o1G1T8eThhMmGILF0NPl9YFp'

    client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)
    client.is_authenticated()
    response = client.secrets.kv.v2.list_secrets(
        mount_point=VAULT_MOUNT_POINT, path='')
    print('Conected to Vault...')

    secrets = {}
    if response and response.get('data') and response['data'].get('keys'):
        secret_keys = response['data']['keys']
        for key in secret_keys:
            secret = (
                client.secrets.kv.v2.read_secret_version(
                    mount_point=VAULT_MOUNT_POINT,
                    path=key,
                )['data']['data'],
            )

            if secret:
                if secret[0][key] == '""':
                    secret[0][key] = ''
                secrets[key] = secret[0][key]
            else:
                print(f'Unable to read secret "{key}"')
    else:
        print(f'No secrets found in "{VAULT_MOUNT_POINT}"')

    def env(key, val_type=None, val=None):
        if key in secrets:
            secret = secrets[key]
            if val_type == bool:
                if secret.lower() == 'false':
                    return False
                return True
            if val_type == int:
                return int(secret)
            if val_type == list:
                return secret.split(',')
            return secret

        if val is None:
            print('ImproperConfigured: ', key)
            return

        return val

except Exception:
    print('Vault access failed, using .env file instead...')

env = environ.Env()
env.read_env(BASE_DIR / '.env')

# TODO: write unit tests
for key in secrets:
    print(key)
    assert env(key) == var(key)


# foo = env("IAAS_API_RETRY_STATUS_CODE_LIST", list, [500, 502, 503, 504])
# print("0: ", foo, type(foo))

# foo = env("DEBUG", bool, False)
# print("0: ", foo, type(foo))

# foo = env("EMAIL_USE_FILE_BACKEND", bool, False)
# print("1: ", foo, type(foo))

# foo = env("EMAIL_HOST", str, "localhost")
# print("2: ", foo, type(foo))

# foo = env("EMAIL_PORT", int, 465)
# print("3: ", foo, type(foo))

# foo = env("EMAIL_PORT", int, True)
# print("4: ", foo, type(foo))

# foo = env("EMAIL_PORT", bool, "465")
# print("5: ", foo, type(foo))

# foo = env("EMAIL_PORT", str, 465)
# print("6: ", foo, type(foo))

# foo = env("REDIS_HOST")
# print("7: ", foo, type(foo))

# foo = env("xxx", bool, "True")
# print("8: ", foo, type(foo))
