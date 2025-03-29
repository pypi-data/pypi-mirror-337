import logging
import re
from pathlib import PurePath

import policy_tool.utils.file_utils as file_utils
from policy_tool.core.policy_assignment_types import PolicyAssignmentType, PolicyType
from policy_tool.core.snowflake_connection_setup import load_snowflake_credentials
from policy_tool.services.policy_configuration_service import PolicyConfigService
from policy_tool.services.policy_solution_service import PolicySolutionClient
from policy_tool.services.snowflake_service import SnowClient, SnowClientConfig
from policy_tool.utils.logger_utils import LoggingAdapter

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
        cmp_naming_convention = self._config.config_dict["NAMING_CONVENTIONS"][
            "COLUMN_MASKING_POLICY_REGEX"
        ]
        rap_naming_convention = self._config.config_dict["NAMING_CONVENTIONS"][
            "ROW_ACCESS_POLICY_REGEX"
        ]

        for cmp in assignments["column_masking_policies"].keys():
            if re.search(cmp_naming_convention, cmp):
                continue
            else:
                raise ValueError(
                    f"Column masking policy {cmp} in project {project} does not follow the naming convention with regex {cmp_naming_convention}"
                )

        for rap in assignments["row_access_policies"].keys():
            if re.search(rap_naming_convention, rap):
                continue
            else:
                raise ValueError(
                    f"Row access policy {rap} in project {project} does not follow the naming convention with regex {rap_naming_convention}"
                )

    def _validate_assignments_on_schema_blacklist(
        self, project: str, assignments_transposed: dict
    ):
        """
        Validate the policy assignments JSONs in regards to the existence of the schemas on the snowflake database.
        Raises an Error if the validation fails.
        """
        project_config = self._config.config_dict["PROJECT_CONFIGS"][project]

        if "POLICY_ASSIGNMENTS_SCHEMA_BLACKLIST" in project_config:
            policy_assignments_schema_blacklist = [
                schema.upper()
                for schema in project_config["POLICY_ASSIGNMENTS_SCHEMA_BLACKLIST"]
            ]
        else:
            policy_assignments_schema_blacklist = []

        for assignment_schema in assignments_transposed["schemas"]:
            if assignment_schema.upper() not in policy_assignments_schema_blacklist:
                continue
            else:
                raise ValueError(
                    f"""
                    Assignment schema {assignment_schema} in project {project} is on the POLICY_ASSIGNMENTS_SCHEMA_BLACKLIST as defined in the config.json file!
                    Please review the defined policy assignments!
                    """
                )

    def _validate_at_least_one_argument_column_rap(
        self, project: str, assignments: dict
    ):
        """
        Validate if at least one argument column is defined for each RAP assignment.
        Raises an Error if the validation fails.
        """
        for rap, rap_assignments in assignments["row_access_policies"].items():
            for assignment_type, rap_assignments_per_type in rap_assignments.items():
                for assignment, argument_columns in rap_assignments_per_type.items():
                    if len(argument_columns) >= 1:
                        continue
                    else:
                        raise ValueError(
                            f"Row access policy {rap} assignment (of type '{assignment_type}') on {assignment} in project {project} does not have at least one argument column defined."
                        )

    def _validate_policy_assignment_uniqueness(
        self, project: str, assignments_transposed: dict
    ):
        """
        Validate the policy assignments JSONs in regards to the uniqueness of assignments on tables/views and columns.
        Note: Only one CMP can be assigned to a specific column and only one RAP to a specific view/table.
        Raises an Error if the validation fails.
        """
        for policy_type in PolicyType:
            for policy_assignment_type in PolicyType.get_assignments_types(policy_type):
                if PolicyAssignmentType.get_policy_assignment_uniqueness(
                    PolicyAssignmentType(policy_assignment_type)
                ):
                    for assignments_object, assignments in assignments_transposed[
                        policy_type.value
                    ][policy_assignment_type].items():
                        if len(assignments) <= 1:
                            continue
                        else:
                            raise ValueError(
                                f"There are multiple {PolicyType.get_policy_type_alternative(policy_type)} assignments defined for {PolicyAssignmentType.get_policy_assignment_singular(PolicyAssignmentType(policy_assignment_type))} {assignments_object.upper()} in project {project}! List of assigned {policy_type.value}: {assignments}!"
                            )

    def _validate_schemas_existence(
        self,
        project: str,
        database: str,
        assignments_transposed: dict,
        snow_client: SnowClient,
        snowflake_role: str,
    ):
        """
        Validate the policy assignments JSONs in regards to the existence of the schemas on the snowflake database.
        Raises an Error if the validation fails.
        """

        snow_client.execute_statement(f"USE DATABASE {database};")

        schemas_metadata, _ = snow_client.execute_query(
            f"SHOW SCHEMAS IN DATABASE {database};"
        )

        schemas = [
            schema["name"]
            for schema in schemas_metadata
            if schema["name"] != "INFORMATION_SCHEMA"
        ]

        for assignment_schema in assignments_transposed["schemas"]:
            if assignment_schema.upper() in schemas:
                continue
            else:
                raise ValueError(
                    f"""
                    Assignment schema {database}.{assignment_schema} in project {project} does not exist on the Snowflake account {self._config.config_dict['SNOWFLAKE_ACCOUNT']}
                    or the executing role {snowflake_role} does not have access to it! Please review the policy assignment JSON files!
                    """
                )

    def _validate_policies_existence(
        self,
        project: str,
        database: str,
        policy_schema: str,
        assignments: dict,
        snow_client: SnowClient,
        snowflake_role: str,
    ):
        """
        Validate the policy assignments JSONs in regards to the existence of the policies on the snowflake database.
        Raises an Error if the validation fails.
        """

        snow_client.execute_statement(f"USE DATABASE {database};")

        cmp_metadata, _ = snow_client.execute_query(
            f"SHOW MASKING POLICIES IN DATABASE {database};"
        )

        rap_metadata, _ = snow_client.execute_query(
            f"SHOW ROW ACCESS POLICIES IN DATABASE {database};"
        )

        cmp_identifiers = [
            f'{cmp["database_name"]}.{cmp["schema_name"]}.{cmp["name"]}'
            for cmp in cmp_metadata
            if cmp["kind"] == "MASKING_POLICY"
        ]

        rap_identifiers = [
            f'{rap["database_name"]}.{rap["schema_name"]}.{rap["name"]}'
            for rap in rap_metadata
            if rap["kind"] == "ROW_ACCESS_POLICY"
        ]

        for cmp in assignments["column_masking_policies"].keys():
            cmp_identifier = f"{database}.{policy_schema}.{cmp}".upper()
            if cmp_identifier in cmp_identifiers:
                continue
            else:
                raise ValueError(
                    f"""
                    Column masking policy {cmp_identifier} in project {project} does not exist on the Snowflake account {self._config.config_dict["SNOWFLAKE_ACCOUNT"]}
                    or the executing role {snowflake_role} does not have access to it!"""
                )
        for rap in assignments["row_access_policies"].keys():
            rap_identifier = f"{database}.{policy_schema}.{rap}".upper()
            if rap_identifier in rap_identifiers:
                continue
            else:
                raise ValueError(
                    f"""
                    Row access policy {rap_identifier} in project {project} does not exist on the Snowflake account {self._config.config_dict["SNOWFLAKE_ACCOUNT"]}
                    or the executing role {snowflake_role} does not have access to it!"""
                )

    def _validate_number_of_assignment_columns(
        self,
        project: str,
        policy_identifier: str,
        policy_type: PolicyType,
        policy_type_as_sql_string: str,
        policy_assignment: str,
        argument_columns: list,
        policy_signature: dict,
    ):
        """
        Validate if the number of columns defined in the policy assignment matches the number of columns in the policy signature.
        Raises an Error if the validation fails.
        """
        if policy_type == PolicyType.COLUMN_MASKING_POLICY:
            n_signature_argument_columns = len(policy_signature) - 1
        elif policy_type == PolicyType.ROW_ACCESS_POLICY:
            n_signature_argument_columns = len(policy_signature)
        else:
            raise ValueError(f"Policy type {policy_type} not supported!")

        if len(argument_columns) != n_signature_argument_columns:
            raise ValueError(
                f"""
                The number of argument columns {len(argument_columns)} for the assignment of {policy_type_as_sql_string} {policy_identifier} on {policy_assignment}
                in project {project} does not match the number of argument columns {n_signature_argument_columns} in the policy signature!
                """
            )

    @staticmethod
    def _get_assignment_object_metadata(
        snow_client: SnowClient,
        policy_type: PolicyType,
        policy_assignment_type: str,
        assignment_object_identifier: str,
    ):
        """
        Get metadata from an Snowflake object for which a policy assignment is defined.
        Uses a "describe"-object query.
        Returns an empty list when no metadata can be retrieved (e.g. when the object does not exist or is not authorized).
        """
        assignment_object_domain = PolicyType.get_object_domain(
            policy_type, policy_assignment_type
        )
        try:
            assignment_object_metadata, _ = snow_client.execute_query(
                f"DESCRIBE {assignment_object_domain} {assignment_object_identifier};"
            )
        except Exception:
            assignment_object_metadata = []

        return assignment_object_metadata

    def _validate_assignment_data_types(
        self,
        project: str,
        database: str,
        policy_identifier: str,
        policy_type: PolicyType,
        policy_type_as_sql_string: str,
        policy_assignment: str,
        policy_assignment_type: str,
        argument_columns: list,
        policy_signature: dict,
        snow_client: SnowClient,
    ):
        if policy_type == PolicyType.COLUMN_MASKING_POLICY:
            assignment_object_identifier = f'{database}.{policy_assignment.split(".")[0]}.{policy_assignment.split(".")[1]}'.upper()
            assignment_columns = [policy_assignment.split(".")[2]] + argument_columns

        elif policy_type == PolicyType.ROW_ACCESS_POLICY:
            assignment_object_identifier = f"{database}.{policy_assignment}".upper()
            assignment_columns = argument_columns
        else:
            raise ValueError(f"Policy type {policy_type} not supported!")

        assignment_object_metadata = self._get_assignment_object_metadata(
            snow_client,
            policy_type,
            policy_assignment_type,
            assignment_object_identifier,
        )

        for i, assignment_column in enumerate(assignment_columns):
            data_type = next(
                (
                    column["type"]
                    for column in assignment_object_metadata
                    if column["name"] == assignment_column.upper()
                ),
                None,
            )

            if data_type:
                data_type_without_precision = data_type.split("(")[0]
                policy_signature_data_type_without_precision = policy_signature[
                    i
                ].split("(")[0]

                if (
                    data_type_without_precision.upper()
                    != policy_signature_data_type_without_precision.upper()
                ):
                    raise ValueError(
                        f"""
                    The data type of argument column {assignment_column} does not match the data type in the policy signature {policy_signature[i]}
                    for the assignment of {policy_type_as_sql_string} {policy_identifier} on {policy_assignment} in project {project} !
                    """
                    )

    @staticmethod
    def _get_policy_signature(
        snow_client: SnowClient, policy_type_as_sql_string: str, policy_identifier: str
    ) -> dict:
        """Query policy information from Snowflake in order to retrieve the signature of the policy containing the data types of all used columns.

        Args:
            snow_client (SnowClient):  Snow Client that contains all operations and information of a Snowflake connection with the Snowflake Python Connector.
            policy_type_as_sql_string (str): Policy type ("MASKING POLICY" or "ROW ACCESS POLICY")
            policy_identifier (str): Full reference of the policy for which the signature should be retrieved.

        Returns:
            policy_signature (dict): Signature of the policy containing the data types of all used columns.
        """
        policy_metadata, _ = snow_client.execute_query(
            f"DESCRIBE {policy_type_as_sql_string} {policy_identifier};"
        )

        policy_signature = {
            i: column.split(" ")[1]
            for i, column in enumerate(
                policy_metadata[0]["signature"][1:-1].split(", ")
            )
        }

        return policy_signature

    def _validate_policy_signatures(
        self,
        project: str,
        database: str,
        policy_schema: str,
        assignments: dict,
        snow_client: SnowClient,
    ):
        snow_client.execute_statement(f"USE DATABASE {database};")

        for policy_type, policy_assignments_per_policy_type in assignments.items():
            policy_type = PolicyType(policy_type)
            policy_type_as_sql_string = PolicyType.get_policy_type_alternative(
                policy_type
            )

            for (
                policy_name,
                policy_assignments,
            ) in policy_assignments_per_policy_type.items():
                policy_identifier = f"{database}.{policy_schema}.{policy_name}".upper()

                policy_signature = self._get_policy_signature(
                    snow_client, policy_type_as_sql_string, policy_identifier
                )

                for (
                    policy_assignment_type,
                    policy_assignments_per_type,
                ) in policy_assignments.items():
                    if policy_assignment_type == PolicyAssignmentType.TAGS.value:
                        continue

                    for (
                        policy_assignment,
                        argument_columns,
                    ) in policy_assignments_per_type.items():
                        self._validate_number_of_assignment_columns(
                            project,
                            policy_identifier,
                            policy_type,
                            policy_type_as_sql_string,
                            policy_assignment,
                            argument_columns,
                            policy_signature,
                        )

                        self._validate_assignment_data_types(
                            project,
                            database,
                            policy_identifier,
                            policy_type,
                            policy_type_as_sql_string,
                            policy_assignment,
                            policy_assignment_type,
                            argument_columns,
                            policy_signature,
                            snow_client,
                        )

    def _validate_policy_assignments_against_snowflake(
        self,
        project: str,
        assignments: dict,
        assignments_transposed: dict,
        environment_selection: int = 0,
    ):
        """
        Additional validation of policy assignments using metadata information from Snowflake.
        """

        project_config = self._config.config_dict["PROJECT_CONFIGS"][project]
        snowflake_role = project_config["SNOWFLAKE_CREDENTIALS"]["ROLE"]
        policy_schema = project_config["POLICY_SCHEMA"]

        for environment, database in project_config["ENVIRONMENTS"].items():
            if environment_selection != 0 and str(environment_selection) != environment:
                continue
            else:
                # connect to snowflake
                snowflake_credentials = load_snowflake_credentials(
                    self._config.config_dict, project, environment
                )
                snowflake_configuration = SnowClientConfig(**snowflake_credentials)

                with SnowClient(snowflake_configuration) as snow_client:
                    self._validate_schemas_existence(
                        project,
                        database,
                        assignments_transposed,
                        snow_client,
                        snowflake_role,
                    )

                    self._validate_policies_existence(
                        project,
                        database,
                        policy_schema,
                        assignments,
                        snow_client,
                        snowflake_role,
                    )

                    self._validate_policy_signatures(
                        project, database, policy_schema, assignments, snow_client
                    )

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
                for policy_assignment_file in self._config.policy_assignments_files[
                    project
                ]:
                    if (
                        file_utils.validate_json(
                            str(assignments_jsonschema_file_path),
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

    def validate_policy_assignments_technical(
        self,
        policy_assignments_jsonschema_folder_path,
        policy_assignments_jsonschema_file_name,
    ):
        """
        Validation of policy assignment JSON files.
        Raises an Error if the validation fails.
        """
        policy_assignments_jsonschema_absolute_folder_path = PurePath(
            self._config.module_root_folder
        ).joinpath(PurePath(policy_assignments_jsonschema_folder_path))

        self._validate_against_json_schema(
            policy_assignments_jsonschema_absolute_folder_path,
            policy_assignments_jsonschema_file_name,
        )

    def validate_policy_assignments_content(self, environment_selection: int = 0):
        """
        Validation of policy assignment JSON files.
        Raises an Error if the validation fails.
        Initializes the PolicySolutionClient as a test to check, e.g., for duplicates and for the naming conventions.
        """

        # initialize policy solution
        policy_solution = PolicySolutionClient(self._config.policy_assignments_files)

        for project, assignments in policy_solution.all_policy_assignments.items():
            assignments_transposed = policy_solution.all_policy_assignments_transposed[
                project
            ]

            self._validate_naming_conventions(project, assignments)

            self._validate_assignments_on_schema_blacklist(
                project, assignments_transposed
            )

            self._validate_at_least_one_argument_column_rap(project, assignments)

            self._validate_policy_assignment_uniqueness(project, assignments_transposed)

            self._validate_policy_assignments_against_snowflake(
                project, assignments, assignments_transposed, environment_selection
            )
