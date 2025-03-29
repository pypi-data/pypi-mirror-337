import logging
import re
import inspect
from pathlib import PurePath
from collections import defaultdict

import policy_tool.utils.file_utils as file_utils
from policy_tool.services.policy_configuration_service import PolicyConfigService
from policy_tool.services.policy_solution_service import PolicySolutionClient
from policy_tool.utils.logger_utils import LoggingAdapter
from policy_tool.services.snowflake_service import SnowClient, SnowClientConfig
from policy_tool.core.snowflake_connection_setup import load_snowflake_credentials


logger = logging.getLogger(__name__)
log = LoggingAdapter(logger)


class PolicyValidationService:
    """
    Class to validate policy assignments on a technical level and on a content level.
    """

    def __init__(self, config: PolicyConfigService):
        self._config = config

    def _validate_naming_conventions(self, project: str, assignments: dict):
        """
        Validate naming conventions of masking policies in the assignments JSONs. 
        Naming conventions are defined in the config JSON files.
        Raises an Error if the validation fails.
        """
        cmp_naming_convention = self._config.config_dict["NAMING_CONVENTIONS"]["COLUMN_MASKING_POLICY_REGEX"]
        rap_naming_convention = self._config.config_dict["NAMING_CONVENTIONS"]["ROW_ACCESS_POLICY_REGEX"]

        for cmp in assignments["column_masking_policies"].keys():
            if re.search(cmp_naming_convention, cmp):
                continue
            else:
                raise ValueError(f"Column masking policy {cmp} in project {project} does not follow the naming convention with regex {cmp_naming_convention}")
            
        for rap in assignments["row_access_policies"].keys():
            if re.search(rap_naming_convention, rap):
                continue
            else:
                raise ValueError(f"Row access policy {rap} in project {project} does not follow the naming convention with regex {rap_naming_convention}")
            
    def _validate_policies_existence(self, project: str, assignments: dict, environment_selection: int = 0):
        """
        Validate the policy assignments JSONs in regards to the existence of the policies on the snowflake database.
        Raises an Error if the validation fails.
        """
        project_config = self._config.config_dict["PROJECT_CONFIGS"][project]
        for environment, database in project_config["ENVIRONMENTS"].items():
            if environment_selection != 0 and str(environment_selection) != environment:
                continue
            else:
                #connect to snowflake
                snowflake_credentials = load_snowflake_credentials(self._config.config_dict, project, environment)
                snowflake_configuration = SnowClientConfig(**snowflake_credentials)

                with SnowClient(snowflake_configuration) as snow_client:

                    snow_client.execute_statement(f"USE DATABASE {database};")

                    cmp_metadata = snow_client.execute_query(f"SHOW MASKING POLICIES IN DATABASE {database};")

                    rap_metadata = snow_client.execute_query(f"SHOW ROW ACCESS POLICIES IN DATABASE {database};")

                    cmp_identifiers = [f'{cmp["database_name"]}.{cmp["schema_name"]}.{cmp["name"]}' for cmp in cmp_metadata if cmp["kind"] == "MASKING_POLICY"]

                    rap_identifiers = [f'{rap["database_name"]}.{rap["schema_name"]}.{rap["name"]}' for rap in rap_metadata if rap["kind"] == "ROW_ACCESS_POLICY"]

                for cmp in assignments["column_masking_policies"].keys():
                    cmp_identifier = f'{database}.{project_config["POLICY_SCHEMA"]}.{cmp}'.upper()
                    if cmp_identifier in cmp_identifiers:
                        continue
                    else:
                        raise ValueError(f'Column masking policy {cmp_identifier} in project {project} does not exist on the Snowflake account {self._config.config_dict["SNOWFLAKE_ACCOUNT"]} or the executing role {project_config["SNOWFLAKE_CREDENTIALS"]["ROLE"]} does not have access to it!')
                for rap in assignments["row_access_policies"].keys():
                    rap_identifier = f'{database}.{project_config["POLICY_SCHEMA"]}.{rap}'.upper()
                    if rap_identifier in rap_identifiers:
                        continue
                    else:
                        raise ValueError(f'Row access policy {rap_identifier} in project {project} does not exist on the Snowflake account {self._config.config_dict["SNOWFLAKE_ACCOUNT"]} or the executing role {project_config["SNOWFLAKE_CREDENTIALS"]["ROLE"]} does not have access to it!')

    def _validate_schemas_existence(self, project: str, assignments_transposed: dict, environment_selection: int = 0):
        """
        Validate the policy assignments JSONs in regards to the existence of the schemas on the snowflake database.
        Raises an Error if the validation fails.
        """
        project_config = self._config.config_dict["PROJECT_CONFIGS"][project]
        for environment, database in project_config["ENVIRONMENTS"].items():
            if environment_selection != 0 and str(environment_selection) != environment:
                continue
            else:
                #connect to snowflake
                snowflake_credentials = load_snowflake_credentials(self._config.config_dict, project, environment)
                snowflake_configuration = SnowClientConfig(**snowflake_credentials)

                with SnowClient(snowflake_configuration) as snow_client:

                    snow_client.execute_statement(f"USE DATABASE {database};")

                    schemas_metadata = snow_client.execute_query(f"SHOW SCHEMAS IN DATABASE {database};")

                    schemas = [schema["name"] for schema in schemas_metadata if schema["name"] != "INFORMATION_SCHEMA"]

                for assignment_schema in assignments_transposed["schemas"]:
                    if assignment_schema.upper() in schemas:
                        continue
                    else:
                        raise ValueError(f'Assignment schema {database}.{assignment_schema} in project {project} does not exist on the Snowflake account {self._config.config_dict["SNOWFLAKE_ACCOUNT"]} or the executing role {project_config["SNOWFLAKE_CREDENTIALS"]["ROLE"]} does not have access to it! Please review the policy assignment JSON files!')

    def _validate_against_json_schema(
        self, jsonschema_absolute_folder_path: str, jsonschema_file_name: str
    ):
        """
        Validate policy assignments JSONs against a JSON schema.
        Raises an Error if the validation fails.
        """
        try:
            assignments_jsonschema_file_path = PurePath(
                jsonschema_absolute_folder_path
            ).joinpath(PurePath(jsonschema_file_name))

            for project in self._config.policy_assignments_files.keys():
                for policy_assignment_file in self._config.policy_assignments_files[project]:
                    if (
                        file_utils.validate_json(
                            assignments_jsonschema_file_path,
                            policy_assignment_file,
                            jsonschema_absolute_folder_path,
                        )
                        is False
                    ):
                        raise EnvironmentError(
                            f"FAILED validation for project {project} of {policy_assignment_file} \n against schema {assignments_jsonschema_file_path}"
                        )
                    else:
                        log.debug(
                            f"------------- SUCCEEDED validation for project {project} of {policy_assignment_file} \n  \
                                                                                            against schema {assignments_jsonschema_file_path}"
                        )

        except Exception as err:
            log.error(str(err))
            raise err

    def validate_policy_assignments_technical(self, policy_assignments_jsonschema_folder_path, policy_assignments_jsonschema_file_name):
        """
            Validation of policy assignments JSON files.
            Raises an Error if the validation fails.
        """
        policy_assignments_jsonschema_absolute_folder_path = PurePath(self._config.module_root_folder).joinpath(PurePath(policy_assignments_jsonschema_folder_path))
        self._validate_against_json_schema(policy_assignments_jsonschema_absolute_folder_path, policy_assignments_jsonschema_file_name)

    def validate_policy_assignments_content(self):
        """
            Validation of policy assignments JSON files.
            Raises an Error if the validation fails.
            Initializes the PolicySolutionClient as a test to check, e.g., for duplicates and for the naming conventions.
        """

        #initialize policy solution
        policy_solution = PolicySolutionClient(self._config.policy_assignments_files)

        for project, assignments in policy_solution.all_policy_assignments.items():

            assignments_transposed = policy_solution.all_policy_assignments_transposed[project]

            self._validate_naming_conventions(project, assignments)

            self._validate_schemas_existence(project, assignments_transposed)

            self._validate_policies_existence(project, assignments)

            self._validate_policy_assignment_uniqueness(project, assignments_transposed)

    def _validate_policy_assignment_uniqueness(self, project: str, assignments_transposed: dict):
        """
        Validate the policy assignments JSONs in regards to the uniqueness of assignments on tables/views and columns.
        Note: Only one CMP can be assigned to a specific column and only one RAP to a specific view/table.
        Raises an Error if the validation fails.
        """

        for column, cmp_assignments in assignments_transposed["column_masking_policies"]["table_columns"].items():
            if len(cmp_assignments)<=1:
                continue
            else:
                raise ValueError(f"There are multiple CMP assignments defined for table column {column.upper()} in project {project}! List of assigned CMPs: {cmp_assignments}!")
            
        for column, cmp_assignments in assignments_transposed["column_masking_policies"]["view_columns"].items():
            if len(cmp_assignments)<=1:
                continue
            else:
                raise ValueError(f"There are multiple CMP assignments defined for view column {column.upper()} in project {project}! List of assigned CMPs: {cmp_assignments}!")
            
        for table, rap_assignments in assignments_transposed["row_access_policies"]["tables"].items():
            if len(rap_assignments)<=1:
                continue
            else:
                raise ValueError(f"There are multiple RAP assignments defined for table {table.upper()} in project {project}! List of assigned RAPs: {rap_assignments}!")
            
        for view, rap_assignments in assignments_transposed["row_access_policies"]["views"].items():
            if len(rap_assignments)<=1:
                continue
            else:
                raise ValueError(f"There are multiple RAP assignments defined for view {view.upper()} in project {project}! List of assigned RAPs: {rap_assignments}!")
            



        

        