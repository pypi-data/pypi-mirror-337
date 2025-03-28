import os

from dotenv import load_dotenv
from pathlib import Path

#########################################################################################
#########################################################################################

def load_snowflake_credentials(system_configs:dict,system_selection:str)->dict:

    snowflake_params = {
        "account"   : system_configs[system_selection]["ACCOUNT"],
        "user"      : system_configs[system_selection]["USER"],
        "password"  : os.getenv(system_configs[system_selection]["PASSWORD_NAME"]),
        "warehouse" : system_configs[system_selection]["WAREHOUSE"],
        "role"      : system_configs[system_selection]["ROLE"],
        "database"  : system_configs[system_selection]["DATABASE"]
    }

    return snowflake_params