import logging
import setup
import os, sys

current_working_dir = os.getcwd()
sys.path.append(current_working_dir)

from aceaccount import configuration, main
from aceutils.logger import LoggingAdapter
from aceaccount.services.account_objects_validation_service import (
    AccountValidationService,
    validate_additionally_storage_integration_allowed_locations,
)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("aceaccount")
logger.setLevel(logging.INFO)
log = LoggingAdapter(logger)

logging.getLogger("snowflake.connector").setLevel(logging.WARNING)

setup.setup()
config = configuration.AccountObjectConfig()

######################################################################################
# Testing Params
option = 1 # see below for difference between option 1 and option 2
additonal_validation = True
fetch = True
fetch_grants = True
fetch_tags = True
validate_technical = True
validate_content = True
execute_dryrun = True
execute = True

######################################################################################

if option == 1:
    # Option 1
    # -> using an optional JSON Schema (which would be located in the "setup-repository")
    # e.g. to define separate specific ranges for the allowed values of the Snowflake parameters 
    # can be usefull when there are exceptions defined on the Snowflake Account
    optional_technical_jsonschema_absolute_folder_path = f"{os.getcwd()}/examples/account_objects/json-schemas/account_object_json_schemas/technical_validation/"
    optional_technical_jsonschema_file_name = "account_objects_technical_validation.schema.json"

if option == 2:
    # Option 2
    # -> using the techical validation JSON Schema as defined internally in Aceaccount
    # can be found under resources\json-schemas\account_object_json_schemas\technical_validation\account_objects_technical_validation.schema.json
    optional_technical_jsonschema_absolute_folder_path = None
    optional_technical_jsonschema_file_name = None

if additonal_validation:
    ######################################################################################
    # additional validation
    validate_additionally_storage_integration_allowed_locations(
        config,
        additional_validation_folder_path=f"{os.getcwd()}/examples/account_objects/json-schemas/account_object_json_schemas/content_validation/",
        additional_validation_file_name="additional_validation_config.json",
    )
    ######################################################################################

if fetch:
    ######################################################################################
    # fetch
    logger.info("-------- START: fetch_account_objects -------- ")
    main.fetch_account_objects(
        config,
        output_path="examples/account_objects/output/",
        dialect_json_schema_relative_file_path="../../../../examples/account_objects/json-schemas/account_object_json_schemas/account_objects.schema.json",
        fetch_grants=fetch_grants,
        fetch_tags=fetch_tags,
    )
    logger.info("-------- END: fetch_account_objects -------- \n\n")
    ######################################################################################

if validate_technical:
    ######################################################################################
    # validate technical
    logger.info("-------- START: validate_technical with optional JSON Schema -------- ")
    main.validate_technical(
        config,
        optional_technical_jsonschema_absolute_folder_path=optional_technical_jsonschema_absolute_folder_path,
        optional_technical_jsonschema_file_name=optional_technical_jsonschema_file_name
    )
    logger.info("-------- END: validate_technical with optional JSON Schema -------- \n\n")
    ######################################################################################

if validate_content:
    ######################################################################################
    # validate content
    logger.info("-------- START: validate_content -------- ")
    main.validate_content(
        config,
        content_jsonschema_absolute_folder_path=f"{os.getcwd()}/examples/account_objects/json-schemas/account_object_json_schemas/content_validation/",
        content_jsonschema_file_name="account_objects_content_validation.schema.json",
    )
    logger.info("-------- END: validate_content -------- \n\n")
    ######################################################################################

if execute_dryrun:
    ######################################################################################
    # execute dryrun
    logger.info("-------- START: execute -------- ")
    main.execute(
        config,
        dryrun=True,
        output_sql_statements=True,
        output_path="examples/account_objects/output/",
        optional_technical_jsonschema_absolute_folder_path=optional_technical_jsonschema_absolute_folder_path,
        optional_technical_jsonschema_file_name=optional_technical_jsonschema_file_name
    )
    logger.info("-------- END: execute -------- \n\n")
    ######################################################################################

if execute:
    ######################################################################################
    # execute
    logger.info("-------- START: execute -------- ")
    main.execute(
        config,
        dryrun=False,
        output_sql_statements=True,
        output_path="examples/account_objects/output/",
        optional_technical_jsonschema_absolute_folder_path=optional_technical_jsonschema_absolute_folder_path,
        optional_technical_jsonschema_file_name=optional_technical_jsonschema_file_name
    )
    logger.info("-------- END: execute -------- \n\n")
    ######################################################################################