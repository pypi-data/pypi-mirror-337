import os

from dotenv import load_dotenv
from pathlib import Path

#########################################################################################
#########################################################################################

def load_azure_credentials(system_configs:dict,system_selection:str)->dict:

    azure_params = {
        "Server"    : system_configs[system_selection]["SERVER"],
        "Database"  : system_configs[system_selection]["DATABASE"],
        "User"      : system_configs[system_selection]["USER"],
        "Password"  : os.getenv(system_configs[system_selection]["PASSWORD_NAME"]),
        "Driver"    : system_configs[system_selection]["DRIVER"],
    }

    return azure_params