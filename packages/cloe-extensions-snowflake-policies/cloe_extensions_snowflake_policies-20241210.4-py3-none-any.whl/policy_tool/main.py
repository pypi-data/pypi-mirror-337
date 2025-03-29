import datetime
import json
import logging
import os
import subprocess
import time
from dataclasses import dataclass

from policy_tool.core.snowflake_connection_setup import load_snowflake_credentials
from policy_tool.services.azure_devops_service import (
    create_pr_comment,
    parse_comment_policy_assignments_to_be_ignored,
)
from policy_tool.services.policy_assignment_comparison_service import (
    PolicyAssignmentComparisonService,
)
from policy_tool.services.policy_configuration_service import PolicyConfigService
from policy_tool.services.policy_metadata_service import PolicyMetadataService
from policy_tool.services.policy_solution_service import PolicySolutionClient
from policy_tool.services.policy_validation_service import PolicyValidationService
from policy_tool.services.snowflake_service import SnowClient, SnowClientConfig
from policy_tool.utils.file_utils import save_file
from policy_tool.utils.logger_utils import LoggingAdapter

logger = logging.getLogger(__name__)
log = LoggingAdapter(logger)
log_break = "=" * 80

#########################################################################################
#########################################################################################


@dataclass
class PolicyToolParams:
    config_file_path_env_variable_name: str = "POLICY_PIPELINE_CONFIG_FILE_PATH"
    config_schema_file_path: str = (
        "./resources/json-schemas/configs/configs.schema.json"
    )
    policy_assignments_jsonschema_folder_path: str = (
        "resources/json-schemas/policy_assignments/"
    )
    policy_assignments_jsonschema_file_name: str = "policy_assignments.schema.json"
    sql_folder_path: str = "./resources/sql/"
    policy_assignments_sql_folder_name: str = "execute_policy_assignments_sql_output"
    policy_assignments_to_be_ignored_folder_name: str = (
        "policy_assignments_to_be_ignored"
    )
    policy_assignments_fetch_folder_name: str = "fetch_output"


def execute_policy_assignments(
    dryrun: bool = False,
    output_sql_statements: bool = False,
    output_policy_assignments_to_be_ignored: bool = False,
    output_path: str = "",
    environment_selection: int = 0,
    save_sql_statements_in_history: bool = False,
):
    """
    Assign policies.
    Raises an Error when the assignment fails.
    """
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M_%S")

        # initialize policy config
        policy_config = PolicyConfigService(
            PolicyToolParams.config_file_path_env_variable_name,
            PolicyToolParams.config_schema_file_path,
            PolicyToolParams.sql_folder_path,
        )

        log.info(f"build_reason: {policy_config.build_reason}")

        # initialize policy solution
        policy_solution = PolicySolutionClient(policy_config.policy_assignments_files)

        start_time_execute_policy_assignments = time.time()

        all_policy_assignments_metadata = {}  # type: dict
        # loop over projects and environments
        for (
            project,
            policy_assignments,
        ) in policy_solution.all_policy_assignments.items():
            all_policy_assignments_metadata[project] = {}
            project_config = policy_config.config_dict["PROJECT_CONFIGS"][project]

            if "POLICY_ASSIGNMENTS_SCHEMA_BLACKLIST" in project_config:
                policy_assignments_schema_blacklist = [
                    schema.upper()
                    for schema in project_config["POLICY_ASSIGNMENTS_SCHEMA_BLACKLIST"]
                ]
            else:
                policy_assignments_schema_blacklist = []

            if environment_selection != 0:
                log.info(log_break)
                log.info(
                    f'Selected environment number {environment_selection} with database {project_config["ENVIRONMENTS"][str(environment_selection)]}'
                )
                log.info(f"Schema Blacklist: {policy_assignments_schema_blacklist}")

            for environment, database in project_config["ENVIRONMENTS"].items():
                if (
                    environment_selection != 0
                    and str(environment_selection) != environment
                ):
                    continue
                else:
                    # connect to snowflake
                    snowflake_credentials = load_snowflake_credentials(
                        policy_config.config_dict, project, environment
                    )
                    snowflake_configuration = SnowClientConfig(**snowflake_credentials)

                    with SnowClient(snowflake_configuration) as snow_client:
                        policy_metadata_service = PolicyMetadataService(
                            snow_client, database
                        )
                        (
                            policy_assignments_metadata,
                            policy_assignments_transposed_metadata,
                        ) = policy_metadata_service.get_policy_assignments_metadata(
                            policy_config.max_number_of_threads
                        )

                        all_policy_assignments_metadata[project][
                            database
                        ] = policy_assignments_metadata

                        policy_assignment_comparison_service = PolicyAssignmentComparisonService(
                            snow_client,
                            database,
                            project_config["POLICY_SCHEMA"],
                            policy_assignments,
                            policy_assignments_metadata,
                            policy_assignments_transposed_metadata,
                            policy_assignments_schema_blacklist=policy_assignments_schema_blacklist,
                        )

                        policy_assignment_comparison_service.generate_set_cmp_actions()
                        if project_config["UNASSIGN_ENABLED"]:
                            policy_assignment_comparison_service.generate_unset_cmp_actions()
                        policy_assignment_comparison_service.generate_add_rap_to_object_actions()
                        if project_config["UNASSIGN_ENABLED"]:
                            policy_assignment_comparison_service.generate_drop_rap_from_object_actions()

                        policy_assignments_statements_text = "\n" + "\n".join(
                            filter(
                                None, policy_assignment_comparison_service._action_list
                            )
                        )
                        if not policy_assignments_statements_text:
                            policy_assignments_statements_text = " "

                        if not dryrun:
                            log.info(log_break)
                            log.info(
                                f"Executing the following sql statements regarding the policy assignments for project {project} on database {database}:"
                            )
                            log.info(log_break)
                            log.info(policy_assignments_statements_text)
                            log.info(log_break)

                            start_time_execute_statements = time.time()
                            snow_client.execute_statement(
                                policy_assignment_comparison_service._action_list
                            )
                            end_time_execute_statements = time.time()
                            log.info(
                                f"============= Execution policy assignment statements: {round(end_time_execute_statements - start_time_execute_statements, 2)} seconds"
                            )
                        else:
                            log.info(log_break)
                            log.info(
                                f"The dry-run produced the following sql statements regarding the policy assignments for project {project} on database {database}:"
                            )
                            log.info(log_break)
                            log.info(policy_assignments_statements_text)
                            log.info(log_break)
                            if policy_assignment_comparison_service.warning_removal_of_policy_assignment:
                                logger.warning(
                                    "\n The dry-run produced sql-statements that lead to the removal of policy assignments. Please review the sql-statements and the assignment-files before approving the Pull Request \n Note: The sql-statements can be found in the pipeline artifacts and in the pipeline log."
                                )
                                logger.info(
                                    "##vso[task.complete result=SucceededWithIssues ;]DONE"
                                )

                        if save_sql_statements_in_history:
                            # Pull latest History changes
                            log.info(log_break)
                            logger.info("+++ PULL LATEST HISTORY CHANGES FROM GIT")

                            subprocess.run(
                                [
                                    "git",
                                    "checkout",
                                    f"origin/{policy_config.branch_name}",
                                ]
                            )
                            subprocess.run(["git", "pull", "--no-rebase"])

                        if output_sql_statements:
                            filepath_sql_statements = save_file(
                                output_path,
                                output_folder_name=PolicyToolParams.policy_assignments_sql_folder_name,
                                output_file_name=f"policy_assignments_sql_statements.{project}__{database}__{timestamp}.sql",
                                output_data=policy_assignments_statements_text,
                            )

                            log.info(
                                f"Saved resulting SQL-statements of the policy assignments in file '{filepath_sql_statements}'."
                            )

                        if save_sql_statements_in_history:
                            # Push latest History changes
                            log.info(log_break)
                            logger.info("+++ PUSH LATEST HISTORY CHANGES TO GIT")

                            subprocess.run(
                                [
                                    "git",
                                    "add",
                                    f"output/{PolicyToolParams.policy_assignments_sql_folder_name}/",
                                ]
                            )
                            subprocess.run(
                                [
                                    "git",
                                    "commit",
                                    "-m",
                                    f"Latest Data Patch History Update from the {policy_config.pipeline_name} Pipeline with ID {policy_config.pipeline_id}",
                                ]
                            )
                            subprocess.run(
                                [
                                    "git",
                                    "push",
                                    "-u",
                                    "origin",
                                    f"HEAD:{policy_config.source_branch}",
                                ]
                            )

                            logger.info("+++ DONE SAVING SQL-STATEMENTS HISTORY")
                            log.info(log_break)

                        if output_policy_assignments_to_be_ignored:
                            filepath_policy_assignments_to_be_ignored = save_file(
                                output_path,
                                output_folder_name=PolicyToolParams.policy_assignments_to_be_ignored_folder_name,
                                output_file_name=f"policy_assignments_to_be_ignored.{project}__{database}__{timestamp}.sql",
                                output_data=policy_assignment_comparison_service.policy_assignments_to_be_ignored,
                            )

                            log.info(
                                f"Saved information about ignored policy assignments in file '{filepath_policy_assignments_to_be_ignored}'."
                            )

                            if policy_config.build_reason == "PullRequest":
                                comment_markdown_policy_assignments_to_be_ignored = parse_comment_policy_assignments_to_be_ignored(
                                    policy_assignment_comparison_service.policy_assignments_to_be_ignored,
                                    project,
                                    database,
                                )
                                if comment_markdown_policy_assignments_to_be_ignored:
                                    create_pr_comment(
                                        comment_markdown_policy_assignments_to_be_ignored,
                                        policy_config,
                                    )

        end_time_execute_policy_assignments = time.time()
        log.info(
            f"============= Execution Time execute_policy_assignments: {round(end_time_execute_policy_assignments - start_time_execute_policy_assignments, 2)} seconds"
        )

    except Exception as err:
        log.error(str(err))
        raise err


def validate_technical():
    """
    Technical validation of policy pipeline configuration, policy assignments and policy objects.
    Raises an Error when the validation fails.
    """
    try:
        # initialize policy config
        policy_config = PolicyConfigService(
            PolicyToolParams.config_file_path_env_variable_name,
            PolicyToolParams.config_schema_file_path,
            PolicyToolParams.sql_folder_path,
        )

        # validate config json
        start_time_validate_config_json = time.time()
        policy_config.validate_config()
        end_time_validate_config_json = time.time()
        log.info(
            f"============= Execution Time load and validate config-JSON: {round(end_time_validate_config_json - start_time_validate_config_json, 2)} seconds"
        )

        # initialize policy validation service
        policy_validation_service = PolicyValidationService(policy_config)

        # validate policy assignments technical
        start_time_validate_assignments_technical = time.time()
        policy_validation_service.validate_policy_assignments_technical(
            PolicyToolParams.policy_assignments_jsonschema_folder_path,
            PolicyToolParams.policy_assignments_jsonschema_file_name,
        )
        end_time_validate_assignments_technical = time.time()
        log.info(
            f"============= Execution Time validate_assignments_technical: {round(end_time_validate_assignments_technical - start_time_validate_assignments_technical, 2)} seconds"
        )
    except Exception as err:
        log.error(str(err))
        raise err


def validate_content(environment_selection: int = 0):
    """
    Content related validation of policy assignments and policy objects.
    Raises an Error when the validation fails.
    Initializes the PolicySolutionClient as a test to check, e.g., for duplicates and for the naming conventions.
    """
    try:
        # initialize policy config
        policy_config = PolicyConfigService(
            PolicyToolParams.config_file_path_env_variable_name,
            PolicyToolParams.config_schema_file_path,
            PolicyToolParams.sql_folder_path,
        )

        # initialize policy validation service
        policy_validation_service = PolicyValidationService(policy_config)

        # validate policy assignments content
        start_time_validate_assignments_content = time.time()
        policy_validation_service.validate_policy_assignments_content(
            environment_selection
        )
        end_time_validate_assignments_content = time.time()
        log.info(
            f"============= Execution Time validate_assignments_content: {round(end_time_validate_assignments_content - start_time_validate_assignments_content, 2)} seconds"
        )
    except Exception as err:
        log.error(str(err))
        raise err


def fetch_policy_assignments(
    output_path: str,
    policy_assignments_jsonschema_relative_path: str,
    environment_selection: int = 0,
):
    """
    Function to fetch existing policy assignments from Snowflake for specific projects.
    Raises an Error when the fetching fails.
    """
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M_%S")
        start_time_fetch_policy_assignments = time.time()

        # initialize policy config
        policy_config = PolicyConfigService(
            PolicyToolParams.config_file_path_env_variable_name,
            PolicyToolParams.config_schema_file_path,
            PolicyToolParams.sql_folder_path,
        )

        all_fetched_policy_assignments = {}  # type: dict
        # loop over projects and environments
        for project in policy_config.config_dict["PROJECT_CONFIGS"].keys():
            all_fetched_policy_assignments[project] = {}
            project_config = policy_config.config_dict["PROJECT_CONFIGS"][project]

            if "POLICY_ASSIGNMENTS_SCHEMA_BLACKLIST" in project_config:
                policy_assignments_schema_blacklist = [
                    schema.upper()
                    for schema in project_config["POLICY_ASSIGNMENTS_SCHEMA_BLACKLIST"]
                ]
            else:
                policy_assignments_schema_blacklist = []

            log.info(log_break)
            log.info(f"START fetching policy assignments for project {project}")
            log.info(f"Schema Blacklist: {policy_assignments_schema_blacklist}")

            if environment_selection != 0:
                log.info(
                    f'Selected environment number {environment_selection} with database {project_config["ENVIRONMENTS"][str(environment_selection)]}'
                )

            for environment, database in project_config["ENVIRONMENTS"].items():
                if (
                    environment_selection != 0
                    and str(environment_selection) != environment
                ):
                    continue
                else:
                    # connect to snowflake
                    snowflake_credentials = load_snowflake_credentials(
                        policy_config.config_dict, project, environment
                    )
                    snowflake_configuration = SnowClientConfig(**snowflake_credentials)

                    with SnowClient(snowflake_configuration) as snow_client:
                        policy_metadata_service = PolicyMetadataService(
                            snow_client, database
                        )

                        (
                            policy_assignments_metadata,
                            _,
                        ) = policy_metadata_service.get_policy_assignments_metadata(
                            policy_config.max_number_of_threads,
                            policy_assignments_schema_blacklist,
                        )

                        fetched_policy_assignments = {
                            "$schema": policy_assignments_jsonschema_relative_path
                        }
                        fetched_policy_assignments.update(policy_assignments_metadata)

                        all_fetched_policy_assignments[project][
                            database
                        ] = fetched_policy_assignments

        if output_path:
            os.makedirs(output_path, exist_ok=True)

            for project in all_fetched_policy_assignments:
                for database in all_fetched_policy_assignments[project]:
                    output_folder_path = os.path.join(
                        output_path,
                        PolicyToolParams.policy_assignments_fetch_folder_name,
                    )
                    filepath_policy_assignments = os.path.join(
                        output_folder_path,
                        f"fetched_policy_assignments.{project}__{database}__{timestamp}.json",
                    )
                    logging.info(
                        f"SAVING fetched policy assignments as JSON file in '{filepath_policy_assignments}'"
                    )
                    os.makedirs(output_folder_path, exist_ok=True)
                    with open(filepath_policy_assignments, "w") as f:
                        json.dump(
                            all_fetched_policy_assignments[project][database],
                            f,
                            indent=4,
                        )
        else:
            log.info(
                "No output_path defined. Fetched policy assignments are not saved in a file."
            )

        end_time_fetch_policy_assignments = time.time()
        log.info(
            f"============= Execution Time fetch_policy_assignments: {round(end_time_fetch_policy_assignments - start_time_fetch_policy_assignments, 2)} seconds"
        )

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

        # TODO

        end_time_fetch_policy_objects = time.time()
        log.info(
            f"============= Execution Time fetch_policy_objects: {round(end_time_fetch_policy_objects - start_time_fetch_policy_objects, 2)} seconds"
        )

    except Exception as err:
        log.error(str(err))
        raise err
