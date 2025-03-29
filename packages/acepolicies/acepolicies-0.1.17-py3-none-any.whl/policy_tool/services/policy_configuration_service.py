import os
from typing import Dict, List, Union
from pathlib import PurePath
import policy_tool.utils.file_utils as file_utils



class PolicyConfigService(object):
    """
    Holds policy tool configurations.
    """

    def __init__(self, config_file_path_env_variable_name: str, config_schema_file_path: str, sql_folder_path: str):
        """ """

        self.config_file_path = os.environ.get(config_file_path_env_variable_name)
        self.config_schema_file_path = config_schema_file_path
        self.module_root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.sql_file_path = PurePath(self.module_root_folder).joinpath(PurePath(sql_folder_path))
        self.load_config()
        self.parse_config()

    def load_config(self):

        self.config_dict = file_utils.load_json(self.config_file_path)

    def parse_config(self):
        """
        Parses config file.
        """
        # organize assignment JSON files by projects
        self.policy_assignments_files = {}
        self.projects =[]
        for project, project_configs in self.config_dict["PROJECT_CONFIGS"].items():
            self.projects.append(project)
            if project not in self.policy_assignments_files:
                self.policy_assignments_files[project]=[]
            self.policy_assignments_files[project] = self.policy_assignments_files[project] + project_configs["POLICY_ASSIGNMENTS_FILES"]

        self.max_number_of_threads = self.config_dict["MAX_NUMBER_OF_THREADS"]

        


    @staticmethod
    def _get_nested_dict_value(
        nested_dict: Dict, keys: List[str], default: str = None
    ) -> str:
        data = nested_dict
        for k in keys:
            if k in data:
                data = data[k]
            else:
                return default
        return data

    def _get_env_var(self, val: str) -> Union[str, bool]:
        """
            If the given value is enclosed with '@@', load value from environment variable of that name.
            Else, return the value.
            If the environment variable value is the string representation of a boolean, return that boolean.
        Args:
            val: str - environment variable name enclosed in '@@', or value
        Raises:
            ValueError - if secret was not found in configured Key Vault
        Returns:
            if value is not marked as name of environment variable: value
            if value is marked as name of environment variable:
                if environment variable is found - will return the environment variable value
                if environment variable is not found - ValueError
        """
        char_delimiter = "@@"

        if (isinstance(val, str) and val.startswith(char_delimiter) and val.endswith(char_delimiter)):
            env_var_name = val[len(char_delimiter) : -len(char_delimiter)]
            env_var_value = self.key_service.get_secret(env_var_name)
            if env_var_value in ["True", "TRUE", "true"]:
                return True
            elif env_var_value in ["False", "FALSE", "false"]:
                return False
            else:
                return env_var_value
        else:
            return val
        
    def validate_config(self):
        """
            Validation of the policy tool configuration.
            Raises an Error when the validation fails.
        """

        config_schema_absolute_file_path = PurePath(self.module_root_folder).joinpath(PurePath(self.config_schema_file_path))
        
        file_utils.validate_json(config_schema_absolute_file_path, self.config_file_path)
