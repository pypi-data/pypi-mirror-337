import os

from dotenv import load_dotenv
from pathlib import Path
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization
import hashlib


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

    if "PASSWORD_NAME" in system_configs[system_selection]:
        snowflake_params['password'] = os.getenv(system_configs[system_selection]["PASSWORD_NAME"])
    elif "PRIVATE_KEY_NAME" in system_configs[system_selection]:
        if "PRIVATE_KEY_PASSPHRASE_NAME" in system_configs[system_selection]:
            # if private key is encrypted it is decrypted here with provided passphrase
            p_key = serialization.load_pem_private_key(
                os.getenv(system_configs[system_selection]["PRIVATE_KEY_NAME"]).encode('utf-8'),
                password = os.getenv(system_configs[system_selection]["PRIVATE_KEY_PASSPHRASE_NAME"]),
                backend = default_backend()
            )

            pkb  = p_key.private_bytes(
            encoding = serialization.Encoding.DER,
            format = serialization.PrivateFormat.PKCS8,
            encryption_algorithm = serialization.NoEncryption())

            snowflake_params['private_key'] = pkb 
        else:
            # private_key_name = str(os.getenv(system_configs[system_selection]["PRIVATE_KEY_NAME"])).replace("\\n","\n")
            # Replace special escape sequences with literal characters
            private_key_name = os.getenv(system_configs[system_selection]["PRIVATE_KEY_NAME"]).encode('unicode_escape').decode('utf-8')
            print("PRIVATE_KEY_NAME: ", private_key_name)
            hash_object = hashlib.sha256()
            hash_object.update(private_key_name.encode('utf-8'))
            hash_hex = hash_object.hexdigest()
            print("hashed PRIVATE_KEY_NAME: ", hash_hex)
            # with open("rsa_key.p8", "w") as key_file:
            #     key_file.write(private_key_name)

            # with open("rsa_key.p8", "rb") as key:
            #     print("key: ", key.read())
            #     # otherwise use not encrypted private key
            #     p_key= serialization.load_pem_private_key(
            #         key.read().encode('utf-8'),
            #         password=None,
            #         backend=default_backend()
            #     )
            p_key= serialization.load_pem_private_key(
                private_key_name.encode("utf-8"),
                password=None,
                backend=default_backend()
            )

            pkb = p_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption())

            snowflake_params['private_key'] = pkb 
    else:
        raise ValueError("No valid authentication method found. Provide either PASSWORD_NAME or PRIVATE_KEY_NAME.")

    return snowflake_params