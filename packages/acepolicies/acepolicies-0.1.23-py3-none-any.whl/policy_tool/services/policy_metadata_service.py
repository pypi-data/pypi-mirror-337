import logging
import os

from typing import Dict, List, Union

from policy_tool.services.snowflake_service import SnowClient
from policy_tool.utils.logger_utils import LoggingAdapter
import policy_tool.utils.file_utils as file_utils
from policy_tool.utils.parallelization_util import execute_func_in_parallel
from  policy_tool.services.policy_configuration_service import PolicyConfigService


logger = logging.getLogger(__name__)
log = LoggingAdapter(logger)


class PolicyMetadataService:
    """
    Class to query metadata information from snowflake policies.
    """

    def __init__(
        self,
        snow_client: SnowClient,
    ):
        """
            Inits a policy metadata service.
        Args:
            snow_client: SnowClient - provides connection a snowflake database
        """
        self._snow_client = snow_client

    
    def _get_cmp_references(self, cmp_identifiers: list) -> list:
    
        for cmp_identifier in cmp_identifiers:

            get_cmp_references=f"SELECT * FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.POLICY_REFERENCES(POLICY_NAME => '{cmp_identifier}'));"

            cmp_references = self._snow_client.execute_query(get_cmp_references, use_dict_cursor=True)

        return cmp_references

    def _get_rap_references(self, rap_identifiers: list) -> list:
        
        for rap_identifier in rap_identifiers:

            get_rap_references=f"SELECT * FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.POLICY_REFERENCES(POLICY_NAME => '{rap_identifier}'));"

            rap_references = self._snow_client.execute_query(get_rap_references, use_dict_cursor=True)

        return rap_references
    

    def _parse_cmp_rap_references(self, database: str, cmp_references: List[Dict], rap_references: List[Dict]) -> Union[dict, dict]:
        
        policy_assignments = {"column_masking_policies":{}, "row_access_policies": {}}
        policy_assignments_transposed = {
            "column_masking_policies": {"table_columns": {}, "view_columns": {}, "tags": {}},
            "row_access_policies": {"tables": {}, "views": {}},
        }

        for cmp_reference in cmp_references:

            if cmp_reference["POLICY_NAME"] not in policy_assignments["column_masking_policies"]:

                policy_assignments["column_masking_policies"][cmp_reference["POLICY_NAME"]] = {
                                                                                                    "annotations": {},
                                                                                                    "table_columns": {},
                                                                                                    "view_columns": {},
                                                                                                    "tags": []
                                                                                                }

            if cmp_reference["REF_ENTITY_DOMAIN"] == "TAG":
                reference_identifier = f'{cmp_reference["REF_SCHEMA_NAME"]}.{cmp_reference["REF_ENTITY_NAME"]}'
            else:
                reference_identifier = f'{cmp_reference["REF_SCHEMA_NAME"]}.{cmp_reference["REF_ENTITY_NAME"]}.{cmp_reference["REF_COLUMN_NAME"]}'

            if cmp_reference["REF_DATABASE_NAME"] == database.upper() and cmp_reference["REF_ENTITY_DOMAIN"] == "TABLE":

                if reference_identifier not in policy_assignments_transposed["column_masking_policies"]["table_columns"]:

                    policy_assignments_transposed["column_masking_policies"]["table_columns"][reference_identifier]=[]

                arg_column_names = self._snow_client.split_snowflake_list_representation(cmp_reference["REF_ARG_COLUMN_NAMES"])

                policy_assignments["column_masking_policies"][cmp_reference ["POLICY_NAME"]]["table_columns"][reference_identifier] = arg_column_names

                policy_assignments_transposed["column_masking_policies"]["table_columns"][reference_identifier]=(cmp_reference ["POLICY_NAME"])

            if cmp_reference["REF_DATABASE_NAME"] == database.upper() and cmp_reference["REF_ENTITY_DOMAIN"] == "VIEW":

                if reference_identifier not in policy_assignments_transposed["column_masking_policies"]["view_columns"]:

                    policy_assignments_transposed["column_masking_policies"]["view_columns"][reference_identifier]=[]

                arg_column_names = self._snow_client.split_snowflake_list_representation(cmp_reference["REF_ARG_COLUMN_NAMES"])

                policy_assignments["column_masking_policies"][cmp_reference ["POLICY_NAME"]]["view_columns"][f'{cmp_reference["REF_SCHEMA_NAME"]}.{cmp_reference["REF_ENTITY_NAME"]}.{cmp_reference["REF_COLUMN_NAME"]}'] = arg_column_names

                policy_assignments_transposed["column_masking_policies"]["view_columns"][reference_identifier]=(cmp_reference ["POLICY_NAME"])

            if cmp_reference["REF_DATABASE_NAME"] == database.upper() and cmp_reference["REF_ENTITY_DOMAIN"] == "TAG":

                if reference_identifier not in policy_assignments_transposed["column_masking_policies"]["tags"]:

                    policy_assignments_transposed["column_masking_policies"]["tags"][reference_identifier]=[]

                policy_assignments["column_masking_policies"][cmp_reference ["POLICY_NAME"]]["tags"].append(f'{cmp_reference["REF_SCHEMA_NAME"]}.{cmp_reference["REF_ENTITY_NAME"]}')

                policy_assignments_transposed["column_masking_policies"]["tags"][reference_identifier].append(cmp_reference ["POLICY_NAME"])

        for rap_reference in rap_references:

            if rap_reference["POLICY_NAME"] not in policy_assignments["row_access_policies"]:

                policy_assignments["row_access_policies"][rap_reference["POLICY_NAME"]] = {
                                                                                                    "annotations": {},
                                                                                                    "tables": {},
                                                                                                    "views": {}
                                                                                                }
                
            reference_identifier = f'{rap_reference["REF_SCHEMA_NAME"]}.{rap_reference["REF_ENTITY_NAME"]}'

            if rap_reference["REF_DATABASE_NAME"] == database.upper() and rap_reference["REF_ENTITY_DOMAIN"] == "TABLE":

                if reference_identifier not in policy_assignments_transposed["row_access_policies"]["tables"]:

                    policy_assignments_transposed["row_access_policies"]["tables"][reference_identifier]=[]

                arg_column_names = self._snow_client.split_snowflake_list_representation(rap_reference["REF_ARG_COLUMN_NAMES"])

                policy_assignments["row_access_policies"][rap_reference ["POLICY_NAME"]]["tables"] [f'{rap_reference["REF_SCHEMA_NAME"]}.{rap_reference["REF_ENTITY_NAME"]}'] = arg_column_names

                policy_assignments_transposed["row_access_policies"]["tables"][reference_identifier]=(rap_reference ["POLICY_NAME"])

            if rap_reference["REF_DATABASE_NAME"] == database.upper() and rap_reference["REF_ENTITY_DOMAIN"] == "VIEW":

                if reference_identifier not in policy_assignments_transposed["row_access_policies"]["views"]:

                    policy_assignments_transposed["row_access_policies"]["views"][reference_identifier]=[]

                arg_column_names = self._snow_client.split_snowflake_list_representation(rap_reference["REF_ARG_COLUMN_NAMES"])

                policy_assignments["row_access_policies"][rap_reference ["POLICY_NAME"]]["views"] [f'{rap_reference["REF_SCHEMA_NAME"]}.{rap_reference["REF_ENTITY_NAME"]}'] = arg_column_names

                policy_assignments_transposed["row_access_policies"]["views"][reference_identifier]=(rap_reference ["POLICY_NAME"])


        return policy_assignments, policy_assignments_transposed


    def get_policy_assignments_metadata(self, database: str, max_number_of_threads: int = 1) -> Union[dict, dict]:
        
        self._snow_client.execute_statement(f"USE DATABASE {database};")

        cmp_metadata = self._snow_client.execute_query(f"SHOW MASKING POLICIES IN DATABASE {database};")

        rap_metadata = self._snow_client.execute_query(f"SHOW ROW ACCESS POLICIES IN DATABASE {database};")

        cmp_identifiers = [f'{cmp["database_name"]}.{cmp["schema_name"]}.{cmp["name"]}' for cmp in cmp_metadata if cmp["kind"] == "MASKING_POLICY"]

        rap_identifiers =  [f'{rap["database_name"]}.{rap["schema_name"]}.{rap["name"]}' for rap in rap_metadata if rap["kind"] == "ROW_ACCESS_POLICY"]

        if max_number_of_threads <=1:
            self._get_cmp_references(cmp_identifiers)
            self._get_rap_references(rap_identifiers)
        else:
            cmp_references = execute_func_in_parallel(self._get_cmp_references, objects = cmp_identifiers, max_number_of_threads = max_number_of_threads)
            rap_references = execute_func_in_parallel(self._get_rap_references, objects = rap_identifiers, max_number_of_threads = max_number_of_threads)

        policy_assignments, policy_assignments_transposed = self._parse_cmp_rap_references(database, cmp_references, rap_references)

        return policy_assignments, policy_assignments_transposed


