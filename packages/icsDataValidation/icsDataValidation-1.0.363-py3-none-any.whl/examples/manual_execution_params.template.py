#########################################################################################
#########################################################################################
import os

def manual_execution_params():

    # Manual execution: File location of the icsDataValidation configuration
    os.environ["CONFIG_FOLDER_NAME"]                    = 'examples/'
    os.environ["CONFIGURATION_FILE_NAME"]               = 'ics_data_validation_config.json'
    os.environ["MIGRATION_CONFIGURATION_FILE_NAME"]     = 'migration_config.json'

    # Manual execution: File path of the locally stored secrets
    # Syntax: <parameter_name>="<value>" per row
    os.environ["ENV_FILEPATH"]  = ''

    # Manual execution: Testset settings
    os.environ["DATABASE_NAME"] = '' #
    os.environ["SCHEMA_NAME"] = '' #

    os.environ["TESTSET_FILE_NAMES"] = ''  # for no testset define as ''

    os.environ["OBJECT_TYPE_RESTRICTION"] = '' #'include_all', 'include_only_tables', 'include_only_views'

    # Manual execution: Result settings
    os.environ["UPLOAD_RESULT_TO_BLOB"] = '' #boolean: True or False
    os.environ["UPLOAD_RESULT_TO_BUCKET"] = '' #boolean: True or False
    os.environ["UPLOAD_RESULT_TO_RESULT_DATABASE"] = ''#boolean: True or False

    # Manual execution: Pandas Dataframe Comparison restrictions -> -1 for no pandas-df comparison at all
    os.environ["MAX_OBJECT_SIZE"] = str(-1) #-1
    os.environ["MAX_ROW_NUMBER"]  = str(-1) #-1

    # Manual execution: Parallelization of comparison settings
    os.environ["MAX_NUMBER_OF_THREADS"]  = str(1) #1

    # Manual execution: Group-By-Aggregation settings
    os.environ["EXECUTE_GROUP_BY_COMPARISON"] = '' #boolean: True or False
    os.environ["USE_GROUP_BY_COLUMNS"] = '' #boolean: True or False
    os.environ["MIN_GROUP_BY_COUNT_DISTINCT"] = str(2) #2
    os.environ["MAX_GROUP_BY_COUNT_DISTINCT"] = str(5) #5
    os.environ["MAX_GROUP_BY_SIZE"] = str(100000000) #100000000

    # Manual execution: Precision settings
    os.environ["NUMERIC_SCALE"] = str(2)
