import logging

from policy_tool.core.policy_assignment_types import PolicyAssignmentType, PolicyType
from policy_tool.services.snowflake_service import SnowClient
from policy_tool.utils.logger_utils import LoggingAdapter

logger = logging.getLogger(__name__)
log = LoggingAdapter(logger)


class PolicyAssignmentComparisonService(object):
    """
    Compare the state of the policy assignments (current state) to the policy assignments files (desired state).
    """

    def __init__(
        self,
        snow_client: SnowClient,
        database: str,
        policy_schema: str,
        desired_policy_assignments: dict,
        current_policy_assignments: dict,
        current_policy_assignments_transposed: dict,
        policy_assignments_schema_blacklist: list,
    ) -> None:
        self._snow_client = snow_client
        self._database = database
        self._policy_schema = policy_schema
        self._desired_policy_assignments = desired_policy_assignments
        self._current_policy_assignments = current_policy_assignments
        self._current_policy_assignments_transposed = (
            current_policy_assignments_transposed
        )
        self._policy_assignments_schema_blacklist = [
            schema.upper() for schema in policy_assignments_schema_blacklist
        ]
        self._action_list: list = []
        self._cmps_unset_already_covered_by_set_actions: dict = {
            policy_assignment_type: []
            for policy_assignment_type in PolicyType.get_assignments_types(
                PolicyType("column_masking_policies")
            )
        }
        self._raps_drop_already_covered_by_add_actions: dict = {
            policy_assignment_type: []
            for policy_assignment_type in PolicyType.get_assignments_types(
                PolicyType("row_access_policies")
            )
        }
        self.policy_assignments_to_be_ignored: dict = {}
        self.warning_removal_of_policy_assignment = False

    def _append_policy_assignments_to_be_ignored(
        self,
        object_identifier,
        object_type_plural,
        assignment_object,
        policy_assignment,
        assigned_policy_type,
    ):
        """Adds an entry in the policy_assignments_to_be_ignored dictionary under the respective object type."""

        policy_assignment_info = {
            "object_identifier": object_identifier,
            "assignment_object_identifier": assignment_object,
            "policy_assignment": policy_assignment,
            "policy_assignment_type": assigned_policy_type,
        }

        if object_type_plural not in self.policy_assignments_to_be_ignored:
            self.policy_assignments_to_be_ignored[object_type_plural] = [
                policy_assignment_info
            ]
        else:
            self.policy_assignments_to_be_ignored[object_type_plural].append(
                policy_assignment_info
            )

    def _check_object_exists(
        self,
        object_identifier: str,
        object_type: str,
        policy_assignment: str,
        assigned_policy_type: str,
        assignment_object: str = "",
        append_policy_assignments_to_be_ignored: bool = True,
    ) -> bool:
        """Check if an object exists on the Snowflake account. Note: The executing role needs access rights to see the object.
            Appends the list of ignored policy assignments. Appending the list of ignored policy assignments is optional for checking the existence of e.g. argument/conditional columns.

        Args:
            object_identifier (str): Object identifier of the policy assignment with full reference (database and schema). E.g. when the assignment is on a column this parameter defines the object that contains the column.
            object_type (str): Object type. E.g. 'view'
            policy_assignment (str): Assigned policy identifier.
            assigned_policy_type (str): Policy type. E.g. 'RAP'
            assignment_object (str): Assignment object identifier with full reference (database and schema).
            append_policy_assignments_to_be_ignored (bool): On True appends the list of ignored policy assignments.

        Appends:
            dict: Objects that are not found on the Snowflake account sorted by object type.

        Returns:
            bool: True if object exists on the Snowflake account and False if object does not exist on the Snowflake account.
        """
        if not assignment_object:
            assignment_object = object_identifier
        database = object_identifier.split(".")[0].upper()
        schema = object_identifier.split(".")[1].upper()

        if object_type == "table":
            object_type_plural = "tables"
            table_name = object_identifier.split(".")[2].upper()

            query_objects = f"SELECT * FROM {database}.INFORMATION_SCHEMA.TABLES WHERE TABLE_CATALOG = '{database}' AND TABLE_SCHEMA = '{schema}' AND TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME = '{table_name}'  AND IS_DYNAMIC = 'NO' AND IS_ICEBERG = 'NO';"

        elif object_type == "view":
            object_type_plural = "views"
            view_name = object_identifier.split(".")[2].upper()
            query_objects = f"SELECT * FROM {database}.INFORMATION_SCHEMA.VIEWS WHERE TABLE_CATALOG = '{database}' AND TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{view_name}';"

        if object_type == "dynamic_table":
            object_type_plural = "dynamic_tables"
            table_name = object_identifier.split(".")[2].upper()

            query_objects = f"SELECT * FROM {database}.INFORMATION_SCHEMA.TABLES WHERE TABLE_CATALOG = '{database}' AND TABLE_SCHEMA = '{schema}' AND TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME = '{table_name}'  AND IS_DYNAMIC = 'YES' AND IS_ICEBERG = 'NO';"

        elif object_type == "column":
            object_type_plural = "columns"
            object_name = object_identifier.split(".")[2].upper()
            column_name = object_identifier.split(".")[3].upper()

            query_objects = f"SELECT * FROM {database}.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_CATALOG = '{database}' AND TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{object_name}' AND COLUMN_NAME = '{column_name}';"

        elif object_type == "tag":
            object_type_plural = "tags"
            tag_name = object_identifier.split(".")[2].upper()

            query_tags = f"SHOW TAGS IN SCHEMA {database}.{schema} LIMIT 10000;"

            tags_information, query_id = self._snow_client.execute_query(
                query_tags, use_dict_cursor=True
            )

            if len(tags_information) == 10000:
                log.warning(
                    f"Limit of 10000 records for 'SHOW TAGS'-query in schema {database}.{schema} reached! The tag {object_identifier} might be falsely flagged as non-existing!"
                )
            else:
                query_objects = f"SELECT $2 AS TAG_NAME FROM TABLE(RESULT_SCAN('{query_id}')) WHERE TAG_NAME = '{tag_name}';"

        objects_information, _ = self._snow_client.execute_query(
            query_objects, use_dict_cursor=True
        )

        if len(objects_information) == 1:
            object_exists = True
        elif len(objects_information) == 0:
            object_exists = False
        else:
            raise ValueError(
                f"Check for existence of object {object_identifier} produced ambiguous results. Please check query: {query_objects}!"
            )

        if append_policy_assignments_to_be_ignored and not object_exists:
            log.info(
                f"The {object_type} {object_identifier} does not exist on the Snowflake account (yet), {assigned_policy_type} assignment {policy_assignment} will be ignored but added to the policy assignments info."
            )

            self._append_policy_assignments_to_be_ignored(
                object_identifier,
                object_type_plural,
                assignment_object,
                policy_assignment,
                assigned_policy_type,
            )

        return object_exists

    def _check_object_exists_as_different_type(
        self, object_identifier: str, object_type: str
    ):
        """Check if an object exists on the Snowflake account as a different type. Note: The executing role needs access rights to see the object.

        Args:
            object_identifier (str): Object identifier with full references (database and schema).
            object_type (str): Object type.

        Raises an Error if the check fails.
        """
        database = object_identifier.split(".")[0].upper()
        schema = object_identifier.split(".")[1].upper()
        object_name = object_identifier.split(".")[2].upper()

        checks = {
            "TABLE": f"SELECT * FROM {database}.INFORMATION_SCHEMA.TABLES WHERE TABLE_CATALOG = '{database}' AND TABLE_SCHEMA = '{schema}' AND TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME = '{object_name}' AND IS_DYNAMIC = 'NO' AND IS_ICEBERG = 'NO';",
            "VIEW": f"SELECT * FROM {database}.INFORMATION_SCHEMA.VIEWS WHERE TABLE_CATALOG = '{database}' AND TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{object_name}';",
            "DYNAMIC_TABLE": f"SELECT * FROM {database}.INFORMATION_SCHEMA.TABLES WHERE TABLE_CATALOG = '{database}' AND TABLE_SCHEMA = '{schema}' AND TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME = '{object_name}' AND IS_DYNAMIC = 'YES' AND IS_ICEBERG = 'NO';",
        }

        if object_type in checks:
            checks.pop(object_type)
        else:
            raise ValueError(
                f"Object type {object_type} not supported during check if object exists as different type."
            )

        for check_type, query_objects in checks.items():
            objects_information, _ = self._snow_client.execute_query(
                query_objects, use_dict_cursor=True
            )

            if len(objects_information) == 1:
                raise ValueError(
                    f"A policy was assigned to the object {object_identifier} as type {object_type} but the object already exists as a {check_type}. Please adjust the policy assignment JSON accordingly!"
                )
            elif len(objects_information) > 1:
                raise ValueError(
                    f"Check for existence of object {object_identifier} produced ambiguous results. Please check query: {query_objects}!"
                )

    def _check_column_already_attached_to_a_cmp(
        self,
        desired_cmp_assignment_column: str,
        desired_cmp_assignment_type: str,
    ) -> None:
        """Checks if there is currently an assignment on the desired column assignment of an masking policy.
        Appends the list of _cmps_unset_already_covered_by_set_actions.
        """
        if (
            desired_cmp_assignment_column.upper()
            in self._current_policy_assignments_transposed["column_masking_policies"][
                desired_cmp_assignment_type
            ]
        ):
            current_cmp = self._current_policy_assignments_transposed[
                "column_masking_policies"
            ][desired_cmp_assignment_type][desired_cmp_assignment_column.upper()]
            self._cmps_unset_already_covered_by_set_actions[
                desired_cmp_assignment_type
            ].append(current_cmp)

    def _check_object_already_attached_to_a_rap(
        self,
        desired_rap_assignment_object: str,
        desired_rap_assignment_object_domain: str,
    ) -> str:
        """Checks if there is currently an assignment on the desired object assignment of an row access policy.
        Appends the list of _raps_drop_already_covered_by_add_actions.
        """
        if (
            desired_rap_assignment_object.upper()
            in self._current_policy_assignments_transposed["row_access_policies"][
                desired_rap_assignment_object_domain
            ]
        ):
            current_rap = self._current_policy_assignments_transposed[
                "row_access_policies"
            ][desired_rap_assignment_object_domain][
                desired_rap_assignment_object.upper()
            ]
            self._raps_drop_already_covered_by_add_actions[
                desired_rap_assignment_object_domain
            ].append(current_rap)
            return current_rap
        else:
            return ""

    def _get_condition_set_cmp(
        self,
        desired_cmp,
        policy_type,
        policy_assignment_type,
        desired_cmp_assignment,
        desired_arg_columns,
    ) -> bool:
        current_assigned_policies = [
            cmp.upper()
            for cmp in self._current_policy_assignments[policy_type.value].keys()
        ]

        if desired_cmp.upper() in current_assigned_policies:
            if policy_assignment_type != "tags":
                current_policy_assignments = [
                    cmp_assignment.upper()
                    for cmp_assignment in self._current_policy_assignments[
                        policy_type.value
                    ][desired_cmp][policy_assignment_type].keys()
                ]
            elif policy_assignment_type == "tags":
                current_policy_assignments = [
                    cmp_assignment.upper()
                    for cmp_assignment in self._current_policy_assignments[
                        policy_type.value
                    ][desired_cmp][policy_assignment_type]
                ]

        condition_set_cmp = (
            desired_cmp.upper() not in current_assigned_policies
            or desired_cmp_assignment.upper() not in current_policy_assignments
            or (
                sorted(
                    [
                        desired_arg_column.upper()
                        for desired_arg_column in desired_arg_columns
                    ]
                )
                != sorted(
                    [
                        current_arg_column.upper()
                        for current_arg_column in self._current_policy_assignments[
                            policy_type.value
                        ][desired_cmp][policy_assignment_type][
                            desired_cmp_assignment.upper()
                        ]
                    ]
                )
                if policy_assignment_type != "tags"
                else False
            )
        )
        return condition_set_cmp

    def _get_condition_unset_cmp(
        self,
        current_cmp: str,
        policy_type: PolicyType,
        policy_assignment_type: str,
        current_cmp_assignment: str,
    ) -> bool:
        desired_assigned_policies = [
            cmp.upper()
            for cmp in self._desired_policy_assignments[policy_type.value].keys()
        ]
        if current_cmp.upper() in desired_assigned_policies:
            if policy_assignment_type != "tags":
                desired_policy_assignments = [
                    desired_cmp_assignment.upper()
                    for desired_cmp_assignment in self._desired_policy_assignments[
                        policy_type.value
                    ][current_cmp][policy_assignment_type].keys()
                ]
            elif policy_assignment_type == "tags":
                desired_policy_assignments = [
                    desired_cmp_assignment.upper()
                    for desired_cmp_assignment in self._desired_policy_assignments[
                        policy_type.value
                    ][current_cmp][policy_assignment_type]
                ]

        condition_unset_cmp = (
            current_cmp.upper() not in desired_assigned_policies
            or current_cmp_assignment.upper() not in desired_policy_assignments
        ) and (
            current_cmp.upper()
            not in [
                desired_cmp_assignment.upper()
                for desired_cmp_assignment in self._cmps_unset_already_covered_by_set_actions[
                    policy_assignment_type
                ]
            ]
            if policy_assignment_type != "tags"
            else True
        )

        return condition_unset_cmp

    def _get_condition_add_rap(
        self,
        desired_rap: str,
        policy_type: PolicyType,
        policy_assignment_type: str,
        desired_rap_assignment: str,
        desired_arg_columns,
    ):
        condition_add_rap = (
            desired_rap.upper()
            not in [
                rap.upper()
                for rap in self._current_policy_assignments[policy_type.value].keys()
            ]
            or desired_rap_assignment.upper()
            not in [
                current_rap_assignment.upper()
                for current_rap_assignment in self._current_policy_assignments[
                    policy_type.value
                ][desired_rap][policy_assignment_type].keys()
            ]
            or sorted(
                [
                    desired_arg_column.upper()
                    for desired_arg_column in desired_arg_columns
                ]
            )
            != sorted(
                [
                    current_arg_column.upper()
                    for current_arg_column in self._current_policy_assignments[
                        policy_type.value
                    ][desired_rap][policy_assignment_type][
                        desired_rap_assignment.upper()
                    ]
                ]
            )
        )

        return condition_add_rap

    def _get_condition_drop_rap(
        self,
        current_rap: str,
        policy_type: PolicyType,
        policy_assignment_type: str,
        current_rap_assignment: str,
    ) -> bool:
        condition_drop_rap = (
            current_rap.upper()
            not in [
                rap.upper()
                for rap in self._desired_policy_assignments[policy_type.value].keys()
            ]
            or current_rap_assignment.upper()
            not in [
                desired_rap_assignment.upper()
                for desired_rap_assignment in self._desired_policy_assignments[
                    policy_type.value
                ][current_rap][policy_assignment_type].keys()
            ]
        ) and current_rap.upper() not in [
            desired_rap_assignment.upper()
            for desired_rap_assignment in self._raps_drop_already_covered_by_add_actions[
                policy_assignment_type
            ]
        ]

        return condition_drop_rap

    def _create_alter_cmp_using_string(
        self,
        desired_cmp: str,
        column_name: str,
        column_reference: str,
        desired_cmp_assignment: str,
        desired_arg_columns: list,
    ):
        using_string = ""
        if desired_arg_columns:
            using_string = f"{column_name}"
            for arg_column in desired_arg_columns:
                column_identifier = f'{self._database.upper()}.{desired_cmp_assignment.split(".")[0].upper()}.{desired_cmp_assignment.split(".")[1].upper()}.{arg_column.upper()}'
                arg_column_exists = self._check_object_exists(
                    object_identifier=column_identifier,
                    object_type="column",
                    policy_assignment=desired_cmp,
                    assigned_policy_type="CMP",
                    assignment_object=column_reference,
                    append_policy_assignments_to_be_ignored=False,
                )
                if not arg_column_exists:
                    raise ValueError(
                        f"The argument-column {column_identifier} does not exist on the Snowflake account for CMP assignment {desired_cmp}."
                    )
                using_string = f"{using_string}, {arg_column}"
            using_string = f"USING ({using_string})"

        return using_string

    def _get_object_reference(
        self,
        policy_assignment_type: PolicyAssignmentType,
        desired_cmp: str,
        desired_cmp_assignment: str,
        object_domain: str,
    ):
        if (
            PolicyAssignmentType.get_policy_assignment_level(policy_assignment_type)
            == "table_level_object"
        ):
            if len(desired_cmp_assignment.split(".")) != 3:
                raise ValueError(
                    f"Assignment {desired_cmp_assignment} for CMP {desired_cmp} on {object_domain.lower()}-column not correctly defined. Please define as <schema>.<{object_domain.lower()}>.<column>"
                )
            object_reference = f'{self._database}.{desired_cmp_assignment.split(".")[0]}.{desired_cmp_assignment.split(".")[1]}'
            column_reference = f"{self._database}.{desired_cmp_assignment}"
            column_name = desired_cmp_assignment.split(".")[2]

            self._check_object_exists_as_different_type(
                object_identifier=object_reference, object_type=object_domain
            )

        elif (
            PolicyAssignmentType.get_policy_assignment_level(policy_assignment_type)
            == "schema_level_object"
        ):
            if len(desired_cmp_assignment.split(".")) != 2:
                raise ValueError(
                    f"Assignment {desired_cmp_assignment} for CMP {desired_cmp} on TAG not correctly defined. Please define as <schema>.<tag>"
                )
            object_reference = f"{self._database}.{desired_cmp_assignment}"
            column_reference = ""
            column_name = ""

        return object_reference, column_reference, column_name

    def _generate_set_cmp_action(
        self,
        desired_cmp: str,
        policy_type: PolicyType,
        policy_assignment_type: str,
        desired_cmp_assignment: str,
        desired_arg_columns: list,
    ):
        object_domain = PolicyType.get_object_domain(
            policy_type, policy_assignment_type
        )
        skip_assignment = False

        object_reference, column_reference, column_name = self._get_object_reference(
            PolicyAssignmentType(policy_assignment_type),
            desired_cmp,
            desired_cmp_assignment,
            object_domain,
        )

        object_exists = self._check_object_exists(
            object_identifier=object_reference,
            object_type=object_domain.lower(),
            policy_assignment=desired_cmp,
            assigned_policy_type="CMP",
            assignment_object=column_reference,
        )

        if not object_exists:
            skip_assignment = True

        if column_reference and object_exists:
            column_exists = self._check_object_exists(
                object_identifier=column_reference,
                object_type="column",
                policy_assignment=desired_cmp,
                assigned_policy_type="CMP",
                assignment_object=column_reference,
            )
            if not column_exists:
                skip_assignment = True

        if not skip_assignment:
            using_string = self._create_alter_cmp_using_string(
                desired_cmp,
                column_name,
                column_reference,
                desired_cmp_assignment,
                desired_arg_columns,
            )

            if policy_assignment_type != "tags":
                if policy_assignment_type == "dynamictable_columns":
                    alter_object_domain = "TABLE"
                else:
                    alter_object_domain = object_domain

                set_cmp_statement = f"ALTER {alter_object_domain} {object_reference} ALTER COLUMN {column_name} SET MASKING POLICY {self._database}.{self._policy_schema}.{desired_cmp} {using_string} FORCE;"

                self._check_column_already_attached_to_a_cmp(
                    desired_cmp_assignment, policy_assignment_type
                )
            elif policy_assignment_type == "tags":
                set_cmp_statement = f"ALTER TAG {object_reference} SET MASKING POLICY {self._database}.{self._policy_schema}.{desired_cmp};"

            self._action_list.append(set_cmp_statement)

    def _generate_unset_cmp_action(
        self,
        current_cmp: str,
        policy_type: PolicyType,
        policy_assignment_type: str,
        current_cmp_assignment: str,
    ):
        object_domain = PolicyType.get_object_domain(
            policy_type, policy_assignment_type
        )

        if policy_assignment_type != "tags":
            object_reference = f'{self._database}.{current_cmp_assignment.split(".")[0]}.{current_cmp_assignment.split(".")[1]}'
            column = current_cmp_assignment.split(".")[2]

            if policy_assignment_type == "dynamictable_columns":
                alter_object_domain = "TABLE"
            else:
                alter_object_domain = object_domain

            unset_cmp_statement = f"ALTER {alter_object_domain} {object_reference} ALTER COLUMN {column} UNSET MASKING POLICY;"

        if policy_assignment_type == "tags":
            unset_cmp_statement = f"ALTER TAG {current_cmp_assignment} UNSET MASKING POLICY {self._database}.{self._policy_schema}.{current_cmp};"

        self._action_list.append(unset_cmp_statement)

    def _generate_add_rap_action(
        self,
        desired_rap: str,
        policy_type: PolicyType,
        policy_assignment_type: str,
        desired_rap_assignment: str,
        desired_arg_columns: list,
    ):
        object_domain = PolicyType.get_object_domain(
            policy_type, policy_assignment_type
        )
        if len(desired_rap_assignment.split(".")) != 2:
            raise ValueError(
                f"Assignment {desired_rap_assignment} for RAP {desired_rap} on {object_domain} not correctly defined. Please define as <schema>.<{object_domain.lower()}>"
            )

        object_reference = f'{self._database}.{desired_rap_assignment.split(".")[0]}.{desired_rap_assignment.split(".")[1]}'

        self._check_object_exists_as_different_type(
            object_identifier=object_reference, object_type=object_domain
        )

        object_exists = self._check_object_exists(
            object_identifier=object_reference,
            object_type=object_domain.lower(),
            policy_assignment=desired_rap,
            assigned_policy_type="RAP",
            assignment_object=object_reference,
        )

        if object_exists:
            columns_string = ""

            for arg_column in desired_arg_columns:
                column_identifier = f'{self._database.upper()}.{desired_rap_assignment.split(".")[0].upper()}.{desired_rap_assignment.split(".")[1].upper()}.{arg_column.upper()}'
                column_exists = self._check_object_exists(
                    object_identifier=column_identifier,
                    object_type="column",
                    policy_assignment=desired_rap,
                    assigned_policy_type="RAP",
                    assignment_object=object_reference,
                    append_policy_assignments_to_be_ignored=False,
                )
                if not column_exists:
                    raise ValueError(
                        f"The argument-column {column_identifier} does not exist on the Snowflake account for RAP assignment {desired_rap}."
                    )

                columns_string = f"{columns_string}, {arg_column}"
            columns_string = f"ON ({columns_string[2:]})"

            current_rap = self._check_object_already_attached_to_a_rap(
                desired_rap_assignment, policy_assignment_type
            )

            if policy_assignment_type == "dynamictables":
                alter_object_domain = "TABLE"
            else:
                alter_object_domain = object_domain

            if current_rap:
                set_rap_statement = f"ALTER {alter_object_domain} {object_reference} DROP ROW ACCESS POLICY {self._database}.{self._policy_schema}.{current_rap}, ADD ROW ACCESS POLICY {self._database}.{self._policy_schema}.{desired_rap} {columns_string};"
            else:
                set_rap_statement = f"ALTER {alter_object_domain} {object_reference} ADD ROW ACCESS POLICY {self._database}.{self._policy_schema}.{desired_rap} {columns_string};"

            self._action_list.append(set_rap_statement)

    def _generate_drop_rap_action(
        self,
        current_rap: str,
        policy_type: PolicyType,
        policy_assignment_type: str,
        current_rap_assignment: str,
    ):
        object_domain = PolicyType.get_object_domain(
            policy_type, policy_assignment_type
        )
        object_reference = f'{self._database}.{current_rap_assignment.split(".")[0]}.{current_rap_assignment.split(".")[1]}'

        if policy_assignment_type == "dynamictables":
            alter_object_domain = "TABLE"
        else:
            alter_object_domain = object_domain

        unset_rap_statement = f"ALTER {alter_object_domain} {object_reference} DROP ROW ACCESS POLICY {self._database}.{self._policy_schema}.{current_rap};"

        self._action_list.append(unset_rap_statement)

    def generate_set_cmp_actions(self) -> None:
        """
        Get all actions to set masking policies on objects and add them to the action list.
        """
        log.debug("ADD actions of type [ 'SET CMP ON OBJECT' ] to action_list")

        policy_type = PolicyType("column_masking_policies")

        for desired_cmp, desired_cmp_assignments in self._desired_policy_assignments[
            policy_type.value
        ].items():
            for policy_assignment_type in PolicyType.get_assignments_types(policy_type):
                if policy_assignment_type == "tags":
                    desired_cmp_assignments_for_type = {
                        desired_cmp_assignment: []
                        for desired_cmp_assignment in desired_cmp_assignments[
                            policy_assignment_type
                        ]
                    }  # type: dict
                else:
                    desired_cmp_assignments_for_type = desired_cmp_assignments[
                        policy_assignment_type
                    ]
                for (
                    desired_cmp_assignment,
                    desired_arg_columns,
                ) in desired_cmp_assignments_for_type.items():
                    desired_cmp_assignment_schema = desired_cmp_assignment.split(".")[0]
                    if (
                        self._get_condition_set_cmp(
                            desired_cmp,
                            policy_type,
                            policy_assignment_type,
                            desired_cmp_assignment,
                            desired_arg_columns,
                        )
                        and desired_cmp_assignment_schema.upper()
                        not in self._policy_assignments_schema_blacklist
                    ):
                        self._generate_set_cmp_action(
                            desired_cmp,
                            policy_type,
                            policy_assignment_type,
                            desired_cmp_assignment,
                            desired_arg_columns,
                        )

    def generate_unset_cmp_actions(self) -> None:
        """
        Get all actions to unset masking policies from objects and add them to the action list.
        """
        log.debug("ADD actions of type [ 'UNSET CMP ON OBJECT' ] to action_list")

        policy_type = PolicyType("column_masking_policies")

        for current_cmp, current_cmp_assignments in self._current_policy_assignments[
            policy_type.value
        ].items():
            for policy_assignment_type in PolicyType.get_assignments_types(policy_type):
                for current_cmp_assignment in current_cmp_assignments[
                    policy_assignment_type
                ]:
                    current_cmp_assignment_schema = current_cmp_assignment.split(".")[0]

                    if (
                        self._get_condition_unset_cmp(
                            current_cmp,
                            policy_type,
                            policy_assignment_type,
                            current_cmp_assignment,
                        )
                        and current_cmp_assignment_schema.upper()
                        not in self._policy_assignments_schema_blacklist
                    ):
                        self._generate_unset_cmp_action(
                            current_cmp,
                            policy_type,
                            policy_assignment_type,
                            current_cmp_assignment,
                        )
                        self.warning_removal_of_policy_assignment = True

    def generate_add_rap_to_object_actions(self) -> None:
        """
        Get all actions to add row access policies to objects and add them to the action list.
        """
        log.debug("ADD actions of type [ 'ADD RAP TO OBJECT' ] to action_list")

        policy_type = PolicyType("row_access_policies")

        for desired_rap, desired_rap_assignments in self._desired_policy_assignments[
            policy_type.value
        ].items():
            for policy_assignment_type in PolicyType.get_assignments_types(policy_type):
                for (
                    desired_rap_assignment,
                    desired_arg_columns,
                ) in desired_rap_assignments[policy_assignment_type].items():
                    desired_rap_assignment_schema = desired_rap_assignment.split(".")[0]

                    if (
                        self._get_condition_add_rap(
                            desired_rap,
                            policy_type,
                            policy_assignment_type,
                            desired_rap_assignment,
                            desired_arg_columns,
                        )
                        and desired_rap_assignment_schema.upper()
                        not in self._policy_assignments_schema_blacklist
                    ):
                        self._generate_add_rap_action(
                            desired_rap,
                            policy_type,
                            policy_assignment_type,
                            desired_rap_assignment,
                            desired_arg_columns,
                        )

    def generate_drop_rap_from_object_actions(self) -> None:
        """
        Get all actions to drop row access policies from objects and add them to the action list.
        """
        log.debug("ADD actions of type [ 'DROP RAP FROM OBJECT' ] to action_list")

        policy_type = PolicyType("row_access_policies")

        for current_rap, current_rap_assignments in self._current_policy_assignments[
            policy_type.value
        ].items():
            for policy_assignment_type in PolicyType.get_assignments_types(policy_type):
                for current_rap_assignment in current_rap_assignments[
                    policy_assignment_type
                ]:
                    current_rap_assignment_schema = current_rap_assignment.split(".")[0]

                    if (
                        self._get_condition_drop_rap(
                            current_rap,
                            policy_type,
                            policy_assignment_type,
                            current_rap_assignment,
                        )
                        and current_rap_assignment_schema.upper()
                        not in self._policy_assignments_schema_blacklist
                    ):
                        self._generate_drop_rap_action(
                            current_rap,
                            policy_type,
                            policy_assignment_type,
                            current_rap_assignment,
                        )
                        self.warning_removal_of_policy_assignment = True
