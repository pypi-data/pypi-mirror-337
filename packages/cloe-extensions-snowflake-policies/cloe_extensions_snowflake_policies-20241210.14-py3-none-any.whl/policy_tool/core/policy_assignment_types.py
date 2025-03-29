from enum import Enum


class PolicyAssignmentType(Enum):
    """
    Enum for valid policy assignment types. Note: Values should be in lower case.
    """

    TABLE_COLUMNS = "table_columns"
    VIEW_COLUMNS = "view_columns"
    DYNAMICTABLE_COLUMNS = "dynamictable_columns"
    VIEWS = "views"
    TABLES = "tables"
    TAGS = "tags"
    DYNAMICTABLES = "dynamictables"

    @staticmethod
    def get_policy_assignment_uniqueness(policy_assignment_type) -> bool:
        """
        Returns True if the desired policy assignment type defines a unique assignment.
        E.g. only one CMP can be assigned to a specific table column.
        """
        policy_assignment_uniqueness = {
            PolicyAssignmentType.TABLE_COLUMNS: True,
            PolicyAssignmentType.VIEW_COLUMNS: True,
            PolicyAssignmentType.DYNAMICTABLE_COLUMNS: True,
            PolicyAssignmentType.VIEWS: True,
            PolicyAssignmentType.TABLES: True,
            PolicyAssignmentType.TAGS: False,
            PolicyAssignmentType.DYNAMICTABLES: True,
        }

        return policy_assignment_uniqueness[policy_assignment_type]

    @staticmethod
    def get_policy_assignment_singular(policy_assignment_type) -> str:
        """
        Returns singular of the desired policy assignment type.
        """
        policy_assignment_singular = {
            PolicyAssignmentType.TABLE_COLUMNS: "table column",
            PolicyAssignmentType.VIEW_COLUMNS: "view column",
            PolicyAssignmentType.DYNAMICTABLE_COLUMNS: "dynamic table column",
            PolicyAssignmentType.VIEWS: "view",
            PolicyAssignmentType.TABLES: "table",
            PolicyAssignmentType.TAGS: "tag",
            PolicyAssignmentType.DYNAMICTABLES: "dynamic table",
        }

        return policy_assignment_singular[policy_assignment_type]

    @staticmethod
    def get_policy_assignment_level(policy_assignment_type) -> str:
        """
        Returns singular of the desired policy assignment type.
        Currently supported are table-level objects (like columns) and schema-level objects like tables.
        """
        policy_assignment_level = {
            PolicyAssignmentType.TABLE_COLUMNS: "table_level_object",
            PolicyAssignmentType.VIEW_COLUMNS: "table_level_object",
            PolicyAssignmentType.DYNAMICTABLE_COLUMNS: "table_level_object",
            PolicyAssignmentType.VIEWS: "schema_level_object",
            PolicyAssignmentType.TABLES: "schema_level_object",
            PolicyAssignmentType.TAGS: "schema_level_object",
            PolicyAssignmentType.DYNAMICTABLES: "schema_level_object",
        }

        return policy_assignment_level[policy_assignment_type]


class PolicyType(Enum):
    """
    Enum for valid policy types. Note: Values should be in lower case.
    """

    COLUMN_MASKING_POLICY = "column_masking_policies"
    ROW_ACCESS_POLICY = "row_access_policies"

    @staticmethod
    def get_policy_type_alternative(policy_type) -> str:
        """
        For the desired policy type, get type of the policy as an alternative string format with whitespaces.
        This format is e.g. used in SQL statements.
        """
        if policy_type == PolicyType.COLUMN_MASKING_POLICY:
            policy_type_alternative = "MASKING POLICY"
        elif policy_type == PolicyType.ROW_ACCESS_POLICY:
            policy_type_alternative = "ROW ACCESS POLICY"
        else:
            raise ValueError(f"Policy type {policy_type} not supported")
        return policy_type_alternative

    @staticmethod
    def get_assignments_information_structure(policy_type) -> dict:
        """
        For the desired policy type, get the policy assignments information structure which is inline with the policy assignments JSON format.
        """
        assignments_information_structure: dict = {
            "annotations": {},
        }
        if policy_type == PolicyType.COLUMN_MASKING_POLICY:
            assignments_information_structure["table_columns"] = {}
            assignments_information_structure["view_columns"] = {}
            assignments_information_structure["dynamictable_columns"] = {}
            assignments_information_structure["tags"] = []
        elif policy_type == PolicyType.ROW_ACCESS_POLICY:
            assignments_information_structure["tables"] = {}
            assignments_information_structure["views"] = {}
            assignments_information_structure["dynamictables"] = {}
        else:
            raise ValueError(f"Policy type {policy_type} not supported")

        return assignments_information_structure

    @staticmethod
    def get_assignments_types(policy_type) -> list:
        """
        For the desired policy type, get the supported policy assignments types.
        """
        if policy_type == PolicyType.COLUMN_MASKING_POLICY:
            assignment_types = [
                PolicyAssignmentType("table_columns").value,
                PolicyAssignmentType("view_columns").value,
                PolicyAssignmentType("dynamictable_columns").value,
                PolicyAssignmentType("tags").value,
            ]
        elif policy_type == PolicyType.ROW_ACCESS_POLICY:
            assignment_types = [
                PolicyAssignmentType("views").value,
                PolicyAssignmentType("tables").value,
                PolicyAssignmentType("dynamictables").value,
            ]
        else:
            raise ValueError(f"Policy type {policy_type} not supported")

        return assignment_types

    @staticmethod
    def get_assignments_type(policy_type, object_domain) -> PolicyAssignmentType:
        """
        For the desired policy type and the object domain, get the supported policy assignments type.
        """
        if policy_type == PolicyType.COLUMN_MASKING_POLICY and object_domain == "TABLE":
            assignment_type = PolicyAssignmentType("table_columns")
        elif (
            policy_type == PolicyType.COLUMN_MASKING_POLICY and object_domain == "VIEW"
        ):
            assignment_type = PolicyAssignmentType("view_columns")
        elif (
            policy_type == PolicyType.COLUMN_MASKING_POLICY
            and object_domain == "DYNAMIC_TABLE"
        ):
            assignment_type = PolicyAssignmentType("dynamictable_columns")
        elif policy_type == PolicyType.COLUMN_MASKING_POLICY and object_domain == "TAG":
            assignment_type = PolicyAssignmentType("tags")
        elif policy_type == PolicyType.ROW_ACCESS_POLICY and object_domain == "TABLE":
            assignment_type = PolicyAssignmentType("tables")
        elif policy_type == PolicyType.ROW_ACCESS_POLICY and object_domain == "VIEW":
            assignment_type = PolicyAssignmentType("views")
        elif (
            policy_type == PolicyType.ROW_ACCESS_POLICY
            and object_domain == "DYNAMIC_TABLE"
        ):
            assignment_type = PolicyAssignmentType("dynamictables")

        else:
            raise ValueError(
                f"Policy type {policy_type} in combination with object domain {object_domain} not supported."
            )

        return assignment_type

    @staticmethod
    def get_object_domain(policy_type, policy_assignment_type: str) -> str:
        """
        For the desired policy and policy assignment type, get the object domain.
        """
        if (
            policy_type == PolicyType.COLUMN_MASKING_POLICY
            and PolicyAssignmentType(policy_assignment_type)
            == PolicyAssignmentType.TABLE_COLUMNS
        ):
            object_domain = "TABLE"
        elif (
            policy_type == PolicyType.COLUMN_MASKING_POLICY
            and PolicyAssignmentType(policy_assignment_type)
            == PolicyAssignmentType.VIEW_COLUMNS
        ):
            object_domain = "VIEW"
        elif (
            policy_type == PolicyType.COLUMN_MASKING_POLICY
            and PolicyAssignmentType(policy_assignment_type)
            == PolicyAssignmentType.DYNAMICTABLE_COLUMNS
        ):
            object_domain = "DYNAMIC_TABLE"
        elif (
            policy_type == PolicyType.COLUMN_MASKING_POLICY
            and PolicyAssignmentType(policy_assignment_type)
            == PolicyAssignmentType.TAGS
        ):
            object_domain = "TAG"
        elif (
            policy_type == PolicyType.ROW_ACCESS_POLICY
            and PolicyAssignmentType(policy_assignment_type)
            == PolicyAssignmentType.TABLES
        ):
            object_domain = "TABLE"
        elif (
            policy_type == PolicyType.ROW_ACCESS_POLICY
            and PolicyAssignmentType(policy_assignment_type)
            == PolicyAssignmentType.VIEWS
        ):
            object_domain = "VIEW"
        elif (
            policy_type == PolicyType.ROW_ACCESS_POLICY
            and PolicyAssignmentType(policy_assignment_type)
            == PolicyAssignmentType.DYNAMICTABLES
        ):
            object_domain = "DYNAMIC_TABLE"

        else:
            raise ValueError(
                f"Policy type {policy_type} in combination with policy assignment type {policy_assignment_type} not supported."
            )
        return object_domain
