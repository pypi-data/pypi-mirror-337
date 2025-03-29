import json
import logging
import os

import policy_tool.utils.file_utils as file_utils
from policy_tool.core.policy_assignment_types import PolicyType
from policy_tool.utils.logger_utils import LoggingAdapter

logger = logging.getLogger(__name__)
log = LoggingAdapter(logger)


class PolicySolutionClient(object):
    """
    Object that collects all functionality based around the policies assignment JSON files.
    The assignment JSON files are organized by categories/projects.
    """

    def __init__(self, policy_assignments_files: dict) -> None:
        """
            Init a new SolutionClient
        Args:
            assignment_files: dict - assignment JSON files organized by categories/projects
        """
        self.policy_assignments_files = policy_assignments_files
        self.all_policy_assignments: dict = {}
        self.all_policy_assignments_transposed: dict = {}
        self._load_policy_assignments_from_files()

    def _add_policy_assignments_entry(self, project: str):
        """
        Creates an entry in all_policy_assignments and all_policy_assignments_transposed for a specific project and with all supported policy and policy-assignment types.
        """
        if project not in self.all_policy_assignments:
            self.all_policy_assignments[project] = {
                policy_type.value: {} for policy_type in PolicyType
            }

        if project not in self.all_policy_assignments_transposed:
            self.all_policy_assignments_transposed[project] = {
                policy_type.value: {
                    policy_assignment_type: {}
                    for policy_assignment_type in PolicyType.get_assignments_types(
                        policy_type
                    )
                }
                for policy_type in PolicyType
            }
            self.all_policy_assignments_transposed[project]["schemas"] = []

    def _dict_raise_on_duplicates(schema, ordered_pairs):
        """Reject duplicate keys."""
        d = {}
        for k, v in ordered_pairs:
            if k in d:
                raise ValueError("duplicate key: %r" % (k,))
            else:
                d[k] = v
        return d

    def _get_policy_assignments_transposed(
        self,
        policy_name: str,
        policy_type: PolicyType,
        policy_assignments_groups: dict,
        project: str,
    ):
        """
        Get policy assignments in transposed form and create entries in self.all_policy_assignments_transposed - sorted by assignments objects.
        Raises an error if the policy assignment type is not supported.
        """
        for assignment_type, assignments_group in policy_assignments_groups.items():
            if assignment_type.lower() not in PolicyType.get_assignments_types(
                policy_type
            ):
                raise ValueError(
                    f"""Error loading the policy_assignments: '{assignment_type.lower()}' is not in the list of the following supported assignment types: {PolicyType.get_assignments_types(policy_type)}"""
                )

            for assignment in assignments_group:
                assignment = assignment.upper()
                assignment_schema = assignment.split(".")[0]

                if (
                    assignment
                    not in self.all_policy_assignments_transposed[project][
                        policy_type.value
                    ][assignment_type]
                ):
                    self.all_policy_assignments_transposed[project][policy_type.value][
                        assignment_type
                    ][assignment] = []

                    if (
                        assignment_schema
                        not in self.all_policy_assignments_transposed[project][
                            "schemas"
                        ]
                    ):
                        self.all_policy_assignments_transposed[project][
                            "schemas"
                        ].append(assignment_schema)

                self.all_policy_assignments_transposed[project][policy_type.value][
                    assignment_type
                ][assignment].append(policy_name)

    def _get_policy_assignments(
        self,
        policy_name: str,
        policy_type: PolicyType,
        policy_assignments_groups: dict,
        project: str,
    ):
        """
        Get policy assignments and create entries in self.all_policy_assignments - sorted by polices.
        Raises an error if an entry for the policy already exists in self.all_policy_assignments.
        """
        policy_name = policy_name.upper()
        if "annotations" in policy_assignments_groups:
            policy_assignments_groups.pop("annotations")

        if policy_name in self.all_policy_assignments[project][policy_type.value]:
            raise ValueError(
                f"Duplicate policy entry {policy_name} for project {project}."
            )

        self.all_policy_assignments[project][policy_type.value][
            policy_name
        ] = policy_assignments_groups

    def _load_policy_assignments_json_file(
        self, policy_assignments_file: str, project: str
    ) -> dict:
        """
        Load the policy assignments from a JSON file.
        Raises an error if there are duplicate policy entries in the JSON file.
        """
        if not os.path.isfile(policy_assignments_file):
            raise EnvironmentError(
                f"Policy assignment file path [ '{policy_assignments_file}' ] is not valid in project {project}."
            )

        policy_assignments = json.loads(
            file_utils.load_file(policy_assignments_file),
            object_pairs_hook=self._dict_raise_on_duplicates,
        )

        return policy_assignments

    def _get_policy_assignments_information(self, policy_assignments, project) -> None:
        """
        Gets the policy assignments information and caches it in all_policy_assignments and in all_policy_assignments_transposed (in transposed form).
        """
        for policy_type, policy_assignments_info in policy_assignments.items():
            policy_type = PolicyType(policy_type)

            for (
                policy_name,
                assignments_groups,
            ) in policy_assignments_info.items():
                for policy_assignment_type in PolicyType.get_assignments_types(
                    policy_type
                ):
                    if policy_assignment_type not in assignments_groups:
                        assignments_groups[
                            policy_assignment_type
                        ] = PolicyType.get_assignments_information_structure(
                            policy_type
                        )[policy_assignment_type]
                self._get_policy_assignments(
                    policy_name=policy_name,
                    policy_type=policy_type,
                    policy_assignments_groups=assignments_groups,
                    project=project,
                )
                self._get_policy_assignments_transposed(
                    policy_name=policy_name,
                    policy_type=policy_type,
                    policy_assignments_groups=assignments_groups,
                    project=project,
                )

    def _load_policy_assignments_from_files(
        self,
    ) -> None:
        """
        Load the policy assignments from the JSON files.
        Raises an error if there are duplicate policy entries in the JSON files for a specific project.
        """

        for project in self.policy_assignments_files.keys():
            self._add_policy_assignments_entry(project)

            for policy_assignments_file in self.policy_assignments_files[project]:
                policy_assignments = self._load_policy_assignments_json_file(
                    policy_assignments_file, project
                )
                policy_assignments.pop("$schema")

                self._get_policy_assignments_information(policy_assignments, project)
