import logging
import os
import json


import policy_tool.utils.file_utils as file_utils
from policy_tool.utils.logger_utils import LoggingAdapter
from policy_tool.core.policy_assignment_types import PolicyAssignmentType

logger = logging.getLogger(__name__)
log = LoggingAdapter(logger)


class PolicySolutionClient(object):
    """
    Object that collects all functionality based around the policies assignment JSON files.
    The assignment JSON files are organized by categories/projects.
    """


    def __init__(
        self,
        policy_assignments_files: dict
    ) -> None:
        """
            Init a new SolutionClient
        Args:
            assignment_files: dict - assignment JSON files organized by categories/projects
        """
        self.policy_assignments_files = policy_assignments_files
        self.all_policy_assignments = {}
        self.all_policy_assignments_transposed = {}

        self.cmp_assignment_type_mapping = {  # maps the name/key of the dict entry in the policy assignments file to the PolicyAssignmentType
                "table_columns": PolicyAssignmentType.TABLECOLUMNS,
                "view_columns": PolicyAssignmentType.VIEWCOLUMNS,
                "tags": PolicyAssignmentType.TAGS,
            }
        
        self.rap_assignment_type_mapping = {  # maps the name/key of the dict entry in the policy assignments file to the PolicyAssignmentType
                "tables": PolicyAssignmentType.TABLES,
                "views": PolicyAssignmentType.VIEWS,
            }

        self._load_policy_assignments()

    def _dict_raise_on_duplicates(schema, ordered_pairs):
        """Reject duplicate keys."""
        d = {}
        for k, v in ordered_pairs:
            if k in d:
                raise ValueError("duplicate key: %r" % (k,))
            else:
                d[k] = v
        return d

    def _load_policy_assignments(
        self,
    ) -> None:
        """
        Load the policy assignments from the JSON files.
        Raises an error if there are duplicate policy entries in the JSON files for a specific project.
        """
        # validate source file paths
        for project in self.policy_assignments_files.keys():

            if project not in self.all_policy_assignments:
                self.all_policy_assignments[project]={"column_masking_policies":{}, "row_access_policies":{}}

            if project not in self.all_policy_assignments_transposed:
                self.all_policy_assignments_transposed[project]= {
                    "column_masking_policies": {"table_columns": {}, "view_columns": {}, "tags": {}},
                    "row_access_policies": {"tables": {}, "views": {}},
                    "schemas": []
                }
            
            for policy_assignments_file in self.policy_assignments_files[project]:
                if not os.path.isfile(policy_assignments_file):
                    raise EnvironmentError(
                        f"Policy assignment file path [ '{policy_assignments_file}' ] is not valid in project {project}."
                    )

                log.debug(f"------------- LOAD policy assignments from [ '{policy_assignments_file}' ]")
                
                
                policy_assignments = json.loads(
                    file_utils.load_file(policy_assignments_file),
                    object_pairs_hook=self._dict_raise_on_duplicates,
                )
                policy_assignments.pop("$schema")

                for cmp, assignments_groups in policy_assignments["column_masking_policies"].items():
                    assignments_groups.pop("annotations")
                    if cmp in self.all_policy_assignments[project]["column_masking_policies"]:
                        raise ValueError(f"Duplicate policy entry {cmp} for project {project}.")
                    else: 
                        self.all_policy_assignments[project]["column_masking_policies"][cmp]=assignments_groups
                    for assignment_type, assignments_group in assignments_groups.items():
                        if assignment_type and assignment_type.lower() not in self.cmp_assignment_type_mapping:
                            raise ValueError(
                                f"""Error loading the policy_assignments: '{assignment_type.lower()}' is not in the list of the following supported assignment types: {[k for k in self.cmp_assignment_type_mapping]}"""
                            )
                        

                        for assignment in assignments_group:
                            assignment_schema=assignment.split('.')[0]
                            if assignment not in self.all_policy_assignments_transposed[project]["column_masking_policies"][assignment_type]:
                                self.all_policy_assignments_transposed[project]["column_masking_policies"][assignment_type][assignment]=[]
                                if assignment_schema not in self.all_policy_assignments_transposed[project]["schemas"]:
                                    self.all_policy_assignments_transposed[project]["schemas"].append(assignment_schema)
                            self.all_policy_assignments_transposed[project]["column_masking_policies"][assignment_type][assignment].append(cmp)       

                for rap, assignments_groups in policy_assignments["row_access_policies"].items():
                    assignments_groups.pop("annotations")
                    if rap in self.all_policy_assignments[project]["row_access_policies"]:
                        raise ValueError(f"Duplicate policy entry {rap} for project {project}.")
                    else:
                        self.all_policy_assignments[project]["row_access_policies"][rap]=assignments_groups
                    for assignment_type, assignments_group in assignments_groups.items():
                        if assignment_type and assignment_type.lower() not in self.rap_assignment_type_mapping:
                            raise ValueError(
                                f"""Error loading the policy_assignments: '{assignment_type.lower()}' is not in the list of the following supported assignment types: {[k for k in self.rap_assignment_type_mapping]}"""
                            )
                        for assignment in assignments_group:
                            assignment_schema=assignment.split('.')[0]
                            if assignment not in self.all_policy_assignments_transposed[project]["row_access_policies"][assignment_type]:
                                self.all_policy_assignments_transposed[project]["row_access_policies"][assignment_type][assignment]=[]
                                if assignment_schema not in self.all_policy_assignments_transposed[project]["schemas"]:
                                    self.all_policy_assignments_transposed[project]["schemas"].append(assignment_schema)
                            self.all_policy_assignments_transposed[project]["row_access_policies"][assignment_type][assignment].append(rap)    