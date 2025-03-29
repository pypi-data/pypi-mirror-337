import logging
from typing import Dict, List, Union

from policy_tool.core.policy_assignment_types import PolicyAssignmentType, PolicyType
from policy_tool.services.snowflake_service import SnowClient
from policy_tool.utils.logger_utils import LoggingAdapter
from policy_tool.utils.parallelization_util import execute_func_in_parallel

logger = logging.getLogger(__name__)
log = LoggingAdapter(logger)


class PolicyMetadataService:
    """
    Class to query metadata information from snowflake policies.
    """

    def __init__(self, snow_client: SnowClient, database: str):
        """
            Inits a policy metadata service.
        Args:
            snow_client: SnowClient - provides connection a snowflake database
        """
        self._snow_client = snow_client

        self._database = database

        self.policy_assignments: dict = {
            policy_type.value: {} for policy_type in PolicyType
        }

        self.policy_assignments_transposed: dict = {
            policy_type.value: {
                policy_assignment_type: {}
                for policy_assignment_type in PolicyType.get_assignments_types(
                    policy_type
                )
            }
            for policy_type in PolicyType
        }

    def _get_cmp_references(self, cmp_identifiers: list) -> list:
        """
        Get policy references from the Snowflake Information Schema for a list of masking policies.

        Args:
            cmp_identifiers (list): List of masking policy identifiers containing database and schema references.

        Returns:
            list: List of masking policy references.
        """
        cmp_references = []
        for cmp_identifier in cmp_identifiers:
            get_cmp_references = f"SELECT * FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.POLICY_REFERENCES(POLICY_NAME => '{cmp_identifier}'));"

            cmp_references_, _ = self._snow_client.execute_query(
                get_cmp_references, use_dict_cursor=True
            )

            cmp_references.extend(cmp_references_)

        return cmp_references

    def _get_rap_references(self, rap_identifiers: list) -> list:
        """
        Get policy references from the Snowflake Information Schema for a list of row access policies.

        Args:
            rap_identifiers (list): List of row access policy identifiers containing database and schema references.

        Returns:
            list: List of row access policy references.
        """
        rap_references = []
        for rap_identifier in rap_identifiers:
            get_rap_references = f"SELECT * FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.POLICY_REFERENCES(POLICY_NAME => '{rap_identifier}'));"

            rap_references_, _ = self._snow_client.execute_query(
                get_rap_references, use_dict_cursor=True
            )
            rap_references.extend(rap_references_)

        return rap_references

    def _parse_policy_reference(self, policy_reference: dict, policy_type=PolicyType):
        """Parse the metadata information of a policy references that was fetched
        from the Snowflake Account and align it with the JSON format of the assignments files.

        Args:
            policy_reference (dict): Dictionary representing the policy reference metadata from Snowflake.
            policy_type (PolicyType): The type of the Snowflake policy.
        """

        policy_assignment_type = PolicyType.get_assignments_type(
            policy_type, policy_reference["REF_ENTITY_DOMAIN"]
        )

        if (
            PolicyAssignmentType.get_policy_assignment_level(policy_assignment_type)
            == "schema_level_object"
        ):
            reference_identifier = f'{policy_reference["REF_SCHEMA_NAME"]}.{policy_reference["REF_ENTITY_NAME"]}'
        elif (
            PolicyAssignmentType.get_policy_assignment_level(policy_assignment_type)
            == "table_level_object"
        ):
            reference_identifier = f'{policy_reference["REF_SCHEMA_NAME"]}.{policy_reference["REF_ENTITY_NAME"]}.{policy_reference["REF_COLUMN_NAME"]}'

        # add an entry for the policy in the policy assignments information if not yet there
        if (
            policy_reference["POLICY_NAME"]
            not in self.policy_assignments[policy_type.value]
        ):
            self.policy_assignments[policy_type.value][
                policy_reference["POLICY_NAME"]
            ] = PolicyType.get_assignments_information_structure(policy_type)

        # add an entry for the assignments objects in the transposed policy assignments information if not yet there
        if (
            reference_identifier
            not in self.policy_assignments_transposed[policy_type.value][
                policy_assignment_type.value
            ]
        ):
            self.policy_assignments_transposed[policy_type.value][
                policy_assignment_type.value
            ][reference_identifier] = []

        # fill in the policy assignments information
        if policy_assignment_type.name == "TAGS":
            self.policy_assignments[policy_type.value][policy_reference["POLICY_NAME"]][
                policy_assignment_type.value
            ].append(reference_identifier)

            self.policy_assignments_transposed[policy_type.value][
                policy_assignment_type.value
            ][reference_identifier].append(policy_reference["POLICY_NAME"])
        else:
            arg_column_names = self._snow_client.split_snowflake_list_representation(
                policy_reference["REF_ARG_COLUMN_NAMES"]
            )

            self.policy_assignments[policy_type.value][policy_reference["POLICY_NAME"]][
                policy_assignment_type.value
            ][reference_identifier] = arg_column_names

            self.policy_assignments_transposed[policy_type.value][
                policy_assignment_type.value
            ][reference_identifier] = policy_reference["POLICY_NAME"]

    def _parse_cmp_rap_references(
        self,
        cmp_references: List[Dict],
        rap_references: List[Dict],
        policy_assignments_schema_blacklist=[],
    ):
        """Parse the metadata information regarding policy references that was fetched
        from the Snowflake Account and align it with the JSON format of the assignments files.

        Args:
            cmp_references (List[Dict]): List of dictionaries with each dictionary representing one row of the masking policy references metadata from Snowflake.
            rap_references (List[Dict]): List of dictionaries with each dictionary representing one row of the row access policy references metadata from Snowflake.
        """
        log.debug(
            f"Database: {self._database.upper()} -> Number of CMP References: {len(cmp_references)}"
        )

        for cmp_reference in cmp_references:
            if (
                cmp_reference["REF_DATABASE_NAME"] == self._database.upper()
                and cmp_reference["REF_SCHEMA_NAME"].upper()
                not in policy_assignments_schema_blacklist
            ):
                self._parse_policy_reference(
                    policy_reference=cmp_reference,
                    policy_type=PolicyType("column_masking_policies"),
                )

        log.debug(
            f"Database: {self._database.upper()} -> Number of RAP References: {len(rap_references)}"
        )
        for rap_reference in rap_references:
            if (
                rap_reference["REF_DATABASE_NAME"] == self._database.upper()
                and rap_reference["REF_SCHEMA_NAME"].upper()
                not in policy_assignments_schema_blacklist
            ):
                self._parse_policy_reference(
                    policy_reference=rap_reference,
                    policy_type=PolicyType("row_access_policies"),
                )

    def get_policy_assignments_metadata(
        self,
        max_number_of_threads: int = 1,
        policy_assignments_schema_blacklist: list = [],
    ) -> tuple[Union[dict, dict], Union[dict, dict]]:
        self._snow_client.execute_statement(f"USE DATABASE {self._database};")

        cmp_metadata, _ = self._snow_client.execute_query(
            f"SHOW MASKING POLICIES IN DATABASE {self._database};"
        )

        rap_metadata, _ = self._snow_client.execute_query(
            f"SHOW ROW ACCESS POLICIES IN DATABASE {self._database};"
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

        cmp_references = execute_func_in_parallel(
            self._get_cmp_references,
            objects=cmp_identifiers,
            max_number_of_threads=max_number_of_threads,
        )
        rap_references = execute_func_in_parallel(
            self._get_rap_references,
            objects=rap_identifiers,
            max_number_of_threads=max_number_of_threads,
        )

        self._parse_cmp_rap_references(
            cmp_references, rap_references, policy_assignments_schema_blacklist
        )

        return self.policy_assignments, self.policy_assignments_transposed
