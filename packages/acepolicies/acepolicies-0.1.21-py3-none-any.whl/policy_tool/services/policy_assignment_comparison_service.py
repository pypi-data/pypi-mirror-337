import logging
from typing import List

from policy_tool.utils.logger_utils import LoggingAdapter
from policy_tool.services.policy_configuration_service import PolicyConfigService

logger = logging.getLogger(__name__)
log = LoggingAdapter(logger)


class PolicyAssignmentComparisonService(object):
    """
    Compare the state of the policy assignments (current state) to the policy assignments files (desired state).
    """

    def __init__(
        self,
        database: str,
        policy_schema: str,
        desired_policy_assignments: dict,
        current_policy_assingments: dict,
        current_policy_assignments_transposed: dict,

    ) -> None:
        self._database = database
        self._policy_schema = policy_schema
        self._desired_policy_assignments = desired_policy_assignments
        self._current_policy_assignments = current_policy_assingments
        self._current_policy_assignments_transposed = current_policy_assignments_transposed
        self._action_list = []
        self._cmps_unset_already_covered_by_set_actions = {'table_columns':[], 'view_columns':[]}
        self._raps_drop_already_covered_by_add_actions = {'tables':[], 'views':[]}

    def generate_set_cmp_actions(self) -> None:
        """
        Get all actions to set masking policies on objects and add them to the action list.
        """
        log.debug("ADD actions of type [ 'SET CMP ON OBJECT' ] to action_list")
        
        for desired_cmp, desired_cmp_assignments in self._desired_policy_assignments["column_masking_policies"].items():
            for desired_cmp_assignment, desired_arg_columns in desired_cmp_assignments['table_columns'].items():
                if (
                    desired_cmp.upper() not in [cmp.upper() for cmp in self._current_policy_assignments["column_masking_policies"].keys()]
                    or desired_cmp_assignment.upper() not in [cmp_assignment.upper() for cmp_assignment in self._current_policy_assignments["column_masking_policies"][desired_cmp]["table_columns"].keys()]
                    or sorted([desired_arg_column.upper() for desired_arg_column in desired_arg_columns])!= sorted([current_arg_column.upper() for current_arg_column in self._current_policy_assignments["column_masking_policies"][desired_cmp]["table_columns"][desired_cmp_assignment.upper()]])
                ):  

                    if len(desired_cmp_assignment.split(".")) != 3:
                           raise ValueError(f"Assignment {desired_cmp_assignment} for CMP {desired_cmp} on TABLECOLUMN not correctly defined. Please define as <schema>.<table>.<column>")

                    else:
                        table_reference = f'{self._database}.{desired_cmp_assignment.split(".")[0]}.{desired_cmp_assignment.split(".")[1]}'
                        column = desired_cmp_assignment.split(".")[2]

                    using_string=''
                    if desired_arg_columns: 
                        using_string=f"{column}"
                        for arg_column in desired_arg_columns:
                            using_string = f"{using_string}, {arg_column}"
                        using_string = f"USING ({using_string})"


                    set_cmp_statement = f"ALTER TABLE {table_reference} ALTER COLUMN {column} SET MASKING POLICY {self._database}.{self._policy_schema}.{desired_cmp} {using_string} FORCE;"
                    self._action_list.append(set_cmp_statement)

                    self._check_column_already_attached_to_a_cmp(desired_cmp_assignment, 'table_columns')

            for desired_cmp_assignment, desired_arg_columns in desired_cmp_assignments['view_columns'].items():
                if (
                    desired_cmp.upper() not in [cmp.upper() for cmp in self._current_policy_assignments["column_masking_policies"].keys()]
                    or desired_cmp_assignment.upper() not in [cmp_assignment.upper() for cmp_assignment in self._current_policy_assignments["column_masking_policies"][desired_cmp]["view_columns"].keys()]
                    or sorted([desired_arg_column.upper() for desired_arg_column in desired_arg_columns])!= sorted([current_arg_column.upper() for current_arg_column in self._current_policy_assignments["column_masking_policies"][desired_cmp]["view_columns"][desired_cmp_assignment.upper()]])
                ):                    

                    if len(desired_cmp_assignment.split(".")) != 3:
                           raise ValueError(f"Assignment {desired_cmp_assignment} for CMP {desired_cmp} on VIEWCOLUMN not correctly defined. Please define as <schema>.<view>.<column>")

                    else:
                        view_reference = f'{self._database}.{desired_cmp_assignment.split(".")[0]}.{desired_cmp_assignment.split(".")[1]}'
                        column = desired_cmp_assignment.split(".")[2]

                    using_string=''
                    if desired_arg_columns: 
                        using_string=f"{column}"
                        for arg_column in desired_arg_columns:
                            using_string = f"{using_string}, {arg_column}"
                        using_string = f"USING ({using_string})"
                        
                    set_cmp_statement = f"ALTER VIEW {view_reference} ALTER COLUMN {column} SET MASKING POLICY {self._database}.{self._policy_schema}.{desired_cmp} {using_string} FORCE;"
                    self._action_list.append(set_cmp_statement)

                    self._check_column_already_attached_to_a_cmp(desired_cmp_assignment, 'view_columns')

            for desired_cmp_assignment in desired_cmp_assignments['tags']:
                if (
                    desired_cmp.upper() not in [cmp.upper() for cmp in self._current_policy_assignments["column_masking_policies"].keys()]
                    or desired_cmp_assignment.upper() not in [cmp_assignment.upper() for cmp_assignment in self._current_policy_assignments["column_masking_policies"][desired_cmp]["tags"]]
                ):                    

                    if len(desired_cmp_assignment.split(".")) != 2:
                           raise ValueError(f"Assignment {desired_cmp_assignment} for CMP {desired_cmp} on TAG not correctly defined. Please define as <schema>.<tag>")
                    else:
                        tag_reference = f'{self._database}.{desired_cmp_assignment}'
                
                    set_cmp_statement = f"ALTER TAG {tag_reference} SET MASKING POLICY {self._database}.{self._policy_schema}.{desired_cmp};"
                    self._action_list.append(set_cmp_statement)

    def generate_unset_cmp_actions(self) -> None:
        """
        Get all actions to unset masking policies from objects and add them to the action list.
        """
        log.debug("ADD actions of type [ 'UNSET CMP ON OBJECT' ] to action_list")

        for current_cmp, current_cmp_assignments in self._current_policy_assignments["column_masking_policies"].items():
            for current_cmp_assignment in current_cmp_assignments['table_columns']:
                if (
                    (current_cmp.upper() not in [cmp.upper() for cmp in self._desired_policy_assignments["column_masking_policies"].keys()]
                    or current_cmp_assignment.upper() not in [desired_cmp_assignment.upper() for desired_cmp_assignment in self._desired_policy_assignments["column_masking_policies"][current_cmp]["table_columns"].keys()])
                    and current_cmp.upper() not in [desired_cmp_assignment.upper() for desired_cmp_assignment in self._cmps_unset_already_covered_by_set_actions["table_columns"]]
                ):  

                    table_reference = f'{self._database}.{current_cmp_assignment.split(".")[0]}.{current_cmp_assignment.split(".")[1]}'
                    column = current_cmp_assignment.split(".")[2]

                    unset_cmp_statement = f"ALTER TABLE {table_reference} ALTER COLUMN {column} UNSET MASKING POLICY;"
                    self._action_list.append(unset_cmp_statement)

        for current_cmp, current_cmp_assignments in self._current_policy_assignments["column_masking_policies"].items():
            for current_cmp_assignment in current_cmp_assignments['view_columns']:
                if (
                    (current_cmp.upper() not in [cmp.upper() for cmp in self._desired_policy_assignments["column_masking_policies"].keys()]
                    or current_cmp_assignment.upper() not in [desired_cmp_assignment.upper() for desired_cmp_assignment in self._desired_policy_assignments["column_masking_policies"][current_cmp]["view_columns"].keys()])
                    and current_cmp.upper() not in [desired_cmp_assignment.upper() for desired_cmp_assignment in self._cmps_unset_already_covered_by_set_actions["view_columns"]]
                ):  

                    view_reference = f'{self._database}.{current_cmp_assignment.split(".")[0]}.{current_cmp_assignment.split(".")[1]}'
                    column = current_cmp_assignment.split(".")[2]

                    unset_cmp_statement = f"ALTER VIEW {view_reference} ALTER COLUMN {column} UNSET MASKING POLICY;"
                    self._action_list.append(unset_cmp_statement)

        for current_cmp, current_cmp_assignments in self._current_policy_assignments["column_masking_policies"].items():
            for current_cmp_assignment in current_cmp_assignments['tags']:
                if (
                    (current_cmp.upper() not in [cmp.upper() for cmp in self._desired_policy_assignments["column_masking_policies"].keys()]
                    or current_cmp_assignment.upper() not in [desired_cmp_assignment.upper() for desired_cmp_assignment in self._desired_policy_assignments["column_masking_policies"][current_cmp]["tags"]])
                ):  
                    
                    unset_cmp_statement = f"ALTER TAG {current_cmp_assignment} UNSET MASKING POLICY {self._database}.{self._policy_schema}.{current_cmp};"
                    self._action_list.append(unset_cmp_statement)

    def generate_add_rap_to_object_actions(self) -> None:
        """
        Get all actions to add row access policies to objects and add them to the action list.
        """
        log.debug("ADD actions of type [ 'ADD RAP TO OBJECT' ] to action_list")

        for desired_rap, desired_rap_assignments in self._desired_policy_assignments["row_access_policies"].items():
            for desired_rap_assignment, desired_arg_columns in desired_rap_assignments['tables'].items():
                if (
                    desired_rap.upper() not in [rap.upper() for rap in self._current_policy_assignments["row_access_policies"].keys()]
                    or desired_rap_assignment.upper() not in [current_rap_assignment.upper() for current_rap_assignment in self._current_policy_assignments["row_access_policies"][desired_rap]["tables"].keys()]
                    or sorted([desired_arg_column.upper() for desired_arg_column in desired_arg_columns])!= sorted([current_arg_column.upper() for current_arg_column in self._current_policy_assignments["row_access_policies"][desired_rap]["tables"][desired_rap_assignment.upper()]])
                ):  
                    columns_string=''
                    if desired_arg_columns: 
                        for arg_column in desired_arg_columns:
                            columns_string = f"{columns_string}, {arg_column}"
                        columns_string = f"ON ({columns_string[2:]})"

                    if len(desired_rap_assignment.split(".")) != 2:
                           raise ValueError(f"Assignment {desired_rap_assignment} for RAP {desired_rap} on TABLE not correctly defined. Please define as <schema>.<table>")

                    else:
                        table_reference = f'{self._database}.{desired_rap_assignment.split(".")[0]}.{desired_rap_assignment.split(".")[1]}'
                    
                    current_rap = self._check_object_already_attached_to_a_rap(desired_rap_assignment, 'tables')

                    if current_rap:
                        set_rap_statement = f"ALTER TABLE {table_reference} DROP ROW ACCESS POLICY {self._database}.{self._policy_schema}.{current_rap}, ADD ROW ACCESS POLICY {self._database}.{self._policy_schema}.{desired_rap} {columns_string};"
                    else:
                        set_rap_statement = f"ALTER TABLE {table_reference} ADD ROW ACCESS POLICY {self._database}.{self._policy_schema}.{desired_rap} {columns_string};"
                    self._action_list.append(set_rap_statement)

            for desired_rap_assignment, desired_arg_columns in desired_rap_assignments['views'].items():
                if (
                    desired_rap.upper() not in [rap.upper() for rap in self._current_policy_assignments["row_access_policies"].keys()]
                    or desired_rap_assignment.upper() not in [current_rap_assignment.upper() for current_rap_assignment in self._current_policy_assignments["row_access_policies"][desired_rap]["views"].keys()]
                    or sorted([desired_arg_column.upper() for desired_arg_column in desired_arg_columns])!= sorted([current_arg_column.upper() for current_arg_column in self._current_policy_assignments["row_access_policies"][desired_rap]["views"][desired_rap_assignment]])
                ):  
                    columns_string=''
                    if desired_arg_columns: 
                        for arg_column in desired_arg_columns:
                            columns_string = f"{columns_string}, {arg_column}"
                        columns_string = f"ON ({columns_string[2:]})"

                    if len(desired_rap_assignment.split(".")) != 2:
                           raise ValueError(f"Assignment {desired_rap_assignment} for RAP {desired_rap} on VIEW not correctly defined. Please define as <schema>.<view>")
                    else:
                        view_reference = f'{self._database}.{desired_rap_assignment.split(".")[0]}.{desired_rap_assignment.split(".")[1]}'
                    

                    current_rap = self._check_object_already_attached_to_a_rap(desired_rap_assignment, 'views')

                    if current_rap:
                        set_rap_statement = f"ALTER VIEW {view_reference} DROP ROW ACCESS POLICY {self._database}.{self._policy_schema}.{current_rap}, ADD ROW ACCESS POLICY {self._database}.{self._policy_schema}.{desired_rap} {columns_string};"
                    else:
                        set_rap_statement = f"ALTER VIEW {view_reference} ADD ROW ACCESS POLICY {self._database}.{self._policy_schema}.{desired_rap} {columns_string};"
                    self._action_list.append(set_rap_statement)


    def generate_drop_rap_from_object_actions(self) -> None:
        """
        Get all actions to drop row access policies from objects and add them to the action list.
        """
        log.debug("ADD actions of type [ 'DROP RAP FROM OBJECT' ] to action_list")


        for current_rap, current_rap_assignments in self._current_policy_assignments["row_access_policies"].items():
            for current_rap_assignment in current_rap_assignments['tables']:
                if (
                    (current_rap.upper() not in [rap.upper() for rap in self._desired_policy_assignments["row_access_policies"].keys()]
                    or current_rap_assignment.upper() not in [desired_rap_assignment.upper() for desired_rap_assignment in self._desired_policy_assignments["row_access_policies"][current_rap]["tables"].keys()])
                    and current_rap.upper() not in [desired_rap_assignment.upper() for desired_rap_assignment in self._raps_drop_already_covered_by_add_actions["tables"]]
                ):  

                    table_reference = f'{self._database}.{current_rap_assignment.split(".")[0]}.{current_rap_assignment.split(".")[1]}'
                    unset_rap_statement = f"ALTER TABLE {table_reference} DROP ROW ACCESS POLICY {self._database}.{self._policy_schema}.{current_rap};"
                    self._action_list.append(unset_rap_statement)

        for current_rap, current_rap_assignments in self._current_policy_assignments["row_access_policies"].items():
            for current_rap_assignment in current_rap_assignments['views']:
                if (
                    (current_rap.upper() not in [rap.upper() for rap in self._desired_policy_assignments["row_access_policies"].keys()]
                    or current_rap_assignment.upper() not in [desired_rap_assignment.upper() for desired_rap_assignment in self._desired_policy_assignments["row_access_policies"][current_rap]["views"].keys()])
                    and current_rap.upper() not in [desired_rap_assignment.upper() for desired_rap_assignment in self._raps_drop_already_covered_by_add_actions["views"]]
                ):  

                    view_reference = f'{self._database}.{current_rap_assignment.split(".")[0]}.{current_rap_assignment.split(".")[1]}'
                    unset_rap_statement = f"ALTER VIEW {view_reference} DROP ROW ACCESS POLICY {self._database}.{self._policy_schema}.{current_rap};"
                    self._action_list.append(unset_rap_statement)
 
    
    def _check_column_already_attached_to_a_cmp(self, desired_cmp_assignment_column: str, desired_cmp_assignment_object_domain: str) -> None:

        if desired_cmp_assignment_column.upper() in self._current_policy_assignments_transposed["column_masking_policies"][desired_cmp_assignment_object_domain]:
            current_cmp = self._current_policy_assignments_transposed["column_masking_policies"][desired_cmp_assignment_object_domain][desired_cmp_assignment_column.upper()]
            self._cmps_unset_already_covered_by_set_actions[desired_cmp_assignment_object_domain].append(current_cmp)
            
    def _check_object_already_attached_to_a_rap(self, desired_rap_assignment_object: str, desired_rap_assignment_object_domain: str) -> str:

        if desired_rap_assignment_object.upper() in self._current_policy_assignments_transposed["row_access_policies"][desired_rap_assignment_object_domain]:
            current_rap = self._current_policy_assignments_transposed["row_access_policies"][desired_rap_assignment_object_domain][desired_rap_assignment_object.upper()]
            self._raps_drop_already_covered_by_add_actions[desired_rap_assignment_object_domain].append(current_rap)
            return current_rap
        else:
            return ''
