import logging
import datetime
import time
import os
import json
from pathlib import PurePath

from dataclasses import dataclass

import policy_tool.utils.file_utils as file_utils
from policy_tool.services.policy_configuration_service import PolicyConfigService
from policy_tool.services.policy_validation_service import PolicyValidationService
from policy_tool.services.policy_solution_service import PolicySolutionClient
from policy_tool.services.policy_metadata_service import PolicyMetadataService
from policy_tool.services.policy_assignment_comparison_service import PolicyAssignmentComparisonService
from policy_tool.utils.logger_utils import LoggingAdapter
from policy_tool.services.snowflake_service import SnowClient, SnowClientConfig
from policy_tool.core.snowflake_connection_setup import load_snowflake_credentials

logger = logging.getLogger(__name__)
log = LoggingAdapter(logger)

#########################################################################################
#########################################################################################

@dataclass
class PolicyToolParams:
    config_file_path_env_variable_name:str  = 'POLICY_PIPELINE_CONFIG_FILE_PATH'
    config_schema_file_path:str             = './resources/json-schemas/configs/configs.schema.json'
    policy_assignments_jsonschema_folder_path: str  = 'resources/json-schemas/policy_assignments/'
    policy_assignments_jsonschema_file_name: str    = 'policy_assignments.schema.json'
    sql_folder_path: str = './resources/sql/'


def execute_policy_assignments(dryrun: bool = False, output_sql_statements: bool = False, output_path: str = ''):
    """
        Assign policies.
        Raises an Error when the assignment fails.
    """
    #TODO try:

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M_%S")

    #initialize policy config
    policy_config = PolicyConfigService(PolicyToolParams.config_file_path_env_variable_name, PolicyToolParams.config_schema_file_path, PolicyToolParams.sql_folder_path)

    #initialize policy solution
    policy_solution = PolicySolutionClient(policy_config.policy_assignments_files)

    start_time_execute_policy_assignments = time.time()

    all_policy_assignments_metadata = {}        
    #loop over projects and environments
    for project, policy_assignments in policy_solution.all_policy_assignments.items():
        all_policy_assignments_metadata[project]={}
        project_config = policy_config.config_dict["PROJECT_CONFIGS"][project]
        for environment, database in project_config["ENVIRONMENTS"].items():
            #connect to snowflake
            snowflake_credentials = load_snowflake_credentials(policy_config.config_dict, project, environment)
            snowflake_configuration = SnowClientConfig(**snowflake_credentials)

            with SnowClient(snowflake_configuration) as snow_client:
                policy_metadata_service = PolicyMetadataService(snow_client)
                policy_assignments_metadata, policy_assignments_transposed_metadata = policy_metadata_service.get_policy_assignments_metadata(database, policy_config.max_number_of_threads)
                
                all_policy_assignments_metadata[project][database]=policy_assignments_metadata

                policy_assignment_comparison_service = PolicyAssignmentComparisonService(database, project_config["POLICY_SCHEMA"], policy_assignments, policy_assignments_metadata, policy_assignments_transposed_metadata)

                policy_assignment_comparison_service.generate_set_cmp_actions()
                if project_config["UNASSING_ENABLED"]:
                    policy_assignment_comparison_service.generate_unset_cmp_actions()
                policy_assignment_comparison_service.generate_add_rap_to_object_actions()
                if project_config["UNASSING_ENABLED"]:
                    policy_assignment_comparison_service.generate_drop_rap_from_object_actions()

                policy_assignments_statements_text = '\n'+'\n'.join(filter(None,policy_assignment_comparison_service._action_list))
                if not policy_assignments_statements_text:
                    policy_assignments_statements_text = ' '

                if not dryrun:                    
                    log.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    log.info(f"Executing the following sql statements regarding the policy assignments for project {project} on database {database}:")
                    log.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    log.info(policy_assignments_statements_text)
                    log.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

                    start_time_execute_statements = time.time()
                    snow_client.execute_statement(policy_assignment_comparison_service._action_list)
                    end_time_execute_statements = time.time()
                    log.info(f"============= Execution policy assignment statements: {round(end_time_execute_statements - start_time_execute_statements, 2)} seconds")
                else:
                    log.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    log.info(f"The dry-run produced the following sql statements regarding the policy assignments for project {project} on database {database}:")
                    log.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    log.info(policy_assignments_statements_text)
                    log.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

                if output_sql_statements:
                    if output_path:
                        filename_sql_statements = os.path.join(output_path, f"policy_assignments_sql_statements.{project}__{database}__{timestamp}.sql")
                        log.info(f"Saving resulting sql statements of the policy assignments in file '{filename_sql_statements}'.")
                        os.makedirs(output_path, exist_ok=True)
                        with open(filename_sql_statements, 'w') as f:
                            f.write(policy_assignments_statements_text)
                    else:
                        log.info("No output_path defined. Policy assignment sql statements are not saved in a file.")
                


    end_time_execute_policy_assignments = time.time()
    log.info(f"============= Execution Time execute_policy_assignments: {round(end_time_execute_policy_assignments - start_time_execute_policy_assignments, 2)} seconds")

    #TODO except Exception as err:
    #    log.error(str(err))
    #raise err


def validate_technical():
    """
        Technical validation of policy pipeline configuration, policy assignments and policy objects.
        Raises an Error when the validation fails.
    """
    #initialize policy config
    policy_config = PolicyConfigService(PolicyToolParams.config_file_path_env_variable_name, PolicyToolParams.config_schema_file_path, PolicyToolParams.sql_folder_path)

    #validate config json
    start_time_validate_config_json = time.time()
    policy_config.validate_config()
    end_time_validate_config_json = time.time()
    log.info(f"============= Execution Time load and validate config-JSON: {round(end_time_validate_config_json - start_time_validate_config_json, 2)} seconds")

    #initialize policy validation service
    policy_validation_service = PolicyValidationService(policy_config)

    #validate policy assignments technical
    start_time_validate_assignments_technical = time.time()
    policy_validation_service.validate_policy_assignments_technical(PolicyToolParams.policy_assignments_jsonschema_folder_path, PolicyToolParams.policy_assignments_jsonschema_file_name)
    end_time_validate_assignments_technical = time.time()
    log.info(f"============= Execution Time validate_assignments_technical: {round(end_time_validate_assignments_technical - start_time_validate_assignments_technical, 2)} seconds")


def validate_content():   
    """
        Content related validation of policy assignments and policy objects.
        Raises an Error when the validation fails.
        Initializes the PolicySolutionClient as a test to check, e.g., for duplicates and for the naming conventions.
    """
    #initialize policy config
    policy_config = PolicyConfigService(PolicyToolParams.config_file_path_env_variable_name, PolicyToolParams.config_schema_file_path, PolicyToolParams.sql_folder_path)

    #initialize policy validation service
    policy_validation_service = PolicyValidationService(policy_config)

    #validate policy assignments content
    start_time_validate_assignments_content = time.time()
    policy_validation_service.validate_policy_assignments_content()
    end_time_validate_assignments_content = time.time()
    log.info(f"============= Execution Time validate_assignments_content: {round(end_time_validate_assignments_content - start_time_validate_assignments_content, 2)} seconds")
     

def fetch_policy_assignments(output_path:str, policy_assignments_jsonschema_relative_path: str):
    """
        Function to fetch existing policy assignments from Snowflake for specific projects. 
        Raises an Error when the fetching fails.
    """
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M_%S")
        start_time_fetch_policy_assignments = time.time()

        #initialize policy config
        policy_config = PolicyConfigService(PolicyToolParams.config_file_path_env_variable_name, PolicyToolParams.config_schema_file_path, PolicyToolParams.sql_folder_path)
        
        all_fetched_policy_assignments = {}        
        #loop over projects and environments
        for project in policy_config.config_dict["PROJECT_CONFIGS"].keys():
            all_fetched_policy_assignments[project]={}
            project_config = policy_config.config_dict["PROJECT_CONFIGS"][project]
            for environment, database in project_config["ENVIRONMENTS"].items():
                #connect to snowflake
                snowflake_credentials = load_snowflake_credentials(policy_config.config_dict, project, environment)
                snowflake_configuration = SnowClientConfig(**snowflake_credentials)

                with SnowClient(snowflake_configuration) as snow_client:
                    policy_metadata_service = PolicyMetadataService(snow_client)
                    policy_assignments_metadata, policy_assignments_transposed_metadata = policy_metadata_service.get_policy_assignments_metadata(database, policy_config.max_number_of_threads)
                    

                    fetched_policy_assignments = {"$schema":policy_assignments_jsonschema_relative_path}
                    fetched_policy_assignments.update(policy_assignments_metadata)

                    all_fetched_policy_assignments[project][database] = fetched_policy_assignments
                    
        if output_path:
            os.makedirs(output_path, exist_ok=True)

            for project in all_fetched_policy_assignments:
                for database in all_fetched_policy_assignments[project]:
                    filename_policy_assignments = os.path.join(output_path, f"fetched_policy_assignments.{project}__{database}__{timestamp}.json")
                    logging.info(f"SAVING fetched policy assignments as JSON file in '{filename_policy_assignments}'")
                    with open(filename_policy_assignments, 'w') as f:
                        json.dump(all_fetched_policy_assignments[project][database], f, indent=4)
        else:
            log.info("No output_path defined. Fetched policy assignments are not saved in a file.")

        end_time_fetch_policy_assignments = time.time()
        log.info(f"============= Execution Time fetch_policy_assignments: {round(end_time_fetch_policy_assignments - start_time_fetch_policy_assignments, 2)} seconds")

    except Exception as err:
        log.error(str(err))
        raise err


def fetch_policy_objects():
    """
        Function to fetch existing policy objects from Snowflake. 
        Raises an Error when the fetching fails.
    """
    try:
        start_time_fetch_policy_objects = time.time()

        #TODO

        end_time_fetch_policy_objects = time.time()
        log.info(f"============= Execution Time fetch_policy_objects: {round(end_time_fetch_policy_objects - start_time_fetch_policy_objects, 2)} seconds")

    except Exception as err:
        log.error(str(err))
        raise err




                
