import os

from dotenv import load_dotenv
from pathlib import Path
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization

#########################################################################################
#########################################################################################

def load_snowflake_credentials(system_configs:dict,system_selection:str)->dict:

    snowflake_params = {
        "account"   : system_configs[system_selection]["ACCOUNT"],
        "user"      : system_configs[system_selection]["USER"],
        "warehouse" : system_configs[system_selection]["WAREHOUSE"],
        "role"      : system_configs[system_selection]["ROLE"],
        "database"  : system_configs[system_selection]["DATABASE"]
    }

    password_name = os.getenv(system_configs[system_selection]["PASSWORD_NAME"])
    private_key_name = os.getenv(system_configs[system_selection]["PRIVATE_KEY_NAME"])
    private_key_passphrase_name = os.getenv(system_configs[system_selection]["PRIVATE_KEY_PASSPHRASE_NAME"])

    if password_name:
        snowflake_params['password'] = password_name
    elif private_key_name:
        if private_key_passphrase_name:
            # if private key is encrypted it is decrypted here with provided passphrase
            p_key = serialization.load_pem_private_key(
                private_key_name,
                password = private_key_passphrase_name,
                backend = default_backend()
            )

            decrypted_p_key = p_key.private_bytes(
            encoding = serialization.Encoding.DER,
            format = serialization.PrivateFormat.PKCS8,
            encryption_algorithm = serialization.NoEncryption())

            snowflake_params['private_key'] = decrypted_p_key
        else:
            # otherwise use the provided not encrypted private key
            snowflake_params['private_key'] = private_key_name
    else:
        raise ValueError("No valid authentication method found. Provide either PASSWORD_NAME or PRIVATE_KEY_NAME.")

    return snowflake_params