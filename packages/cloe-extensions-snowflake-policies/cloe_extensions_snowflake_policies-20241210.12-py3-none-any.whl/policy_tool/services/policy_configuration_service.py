import os
from pathlib import PurePath
from typing import Dict, List, Optional, Union

import policy_tool.utils.file_utils as file_utils


class PolicyConfigService(object):
    """
    Holds policy tool configurations.
    """

    def __init__(
        self,
        config_file_path_env_variable_name: str,
        config_schema_file_path: str,
        sql_folder_path: str,
    ):
        """ """

        self.config_file_path = os.environ.get(config_file_path_env_variable_name)
        self.config_schema_file_path = config_schema_file_path
        self.module_root_folder = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        self.sql_file_path = PurePath(self.module_root_folder).joinpath(
            PurePath(sql_folder_path)
        )
        self.load_devops_variables()
        self.load_config()
        self.parse_config()

    def load_devops_variables(self):
        self.build_reason = os.environ.get("BUILD_REASON")
        self.build_repository_name = os.environ.get("BUILD_REPOSITORY_NAME")
        self.system_accesstoken = os.environ.get("SYSTEM_ACCESSTOKEN")
        self.system_teamprojectid = os.environ.get("SYSTEM_TEAMPROJECTID")
        self.system_teamfoundationcollectionuri = os.environ.get(
            "SYSTEM_TEAMFOUNDATIONCOLLECTIONURI"
        )
        self.system_pullrequest_pullrequestid = os.environ.get(
            "SYSTEM_PULLREQUEST_PULLREQUESTID"
        )
        self.branch_name = os.environ.get("BRANCH_NAME")
        self.source_branch = os.environ.get("BUILD_SOURCEBRANCH")
        self.pipeline_id = (
            str(os.getenv("BUILD_BUILDNUMBER")).replace("#", "_").replace("-", "_")
        )
        self.pipeline_name = os.environ.get("BUILD_DEFINITIONNAME")

    def load_config(self):
        self.config_dict = file_utils.load_json(self.config_file_path)

    def parse_config(self):
        """
        Parses config file.
        """
        # organize assignment JSON files by projects
        self.policy_assignments_files = {}
        self.projects = []
        for project, project_configs in self.config_dict["PROJECT_CONFIGS"].items():
            self.projects.append(project)
            if project not in self.policy_assignments_files:
                self.policy_assignments_files[project] = []
            self.policy_assignments_files[project] = (
                self.policy_assignments_files[project]
                + project_configs["POLICY_ASSIGNMENTS_FILES"]
            )

        self.max_number_of_threads = self.config_dict["MAX_NUMBER_OF_THREADS"]
        self.snowflake_account_name = self.config_dict["SNOWFLAKE_ACCOUNT_NAME"]

    @staticmethod
    def _get_nested_dict_value(
        nested_dict: Dict, keys: List[str], default: Optional[str] = None
    ) -> Union[dict, Optional[str]]:
        data = nested_dict
        for k in keys:
            if k in data:
                data = data[k]
            else:
                return default
        return data

    def validate_config(self):
        """
        Validation of the policy tool configuration.
        Raises an Error when the validation fails.
        """

        config_schema_absolute_file_path = PurePath(self.module_root_folder).joinpath(
            PurePath(self.config_schema_file_path)
        )

        file_utils.validate_json(
            config_schema_absolute_file_path, self.config_file_path
        )
