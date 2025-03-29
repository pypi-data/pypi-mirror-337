from unittest.mock import MagicMock, Mock

import pytest

from policy_tool.core.policy_assignment_types import PolicyType
from policy_tool.services.policy_validation_service import PolicyValidationService
from policy_tool.services.snowflake_service import SnowClient, SnowClientConfig


@pytest.fixture
def policy_config_service():
    config = Mock()
    config.config_dict = {
        "NAMING_CONVENTIONS": {
            "COLUMN_MASKING_POLICY_REGEX": "^MP_.*$|MY_MASKING_POLICY",
            "ROW_ACCESS_POLICY_REGEX": "^RAP_.*$",
        },
        "SNOWFLAKE_CREDENTIALS": {
            "account": "test_account",
            "user": "test_user",
            "password": "test_password",
            "database": "test_db",
            "schema": "test_schema",
        },
    }
    return config


@pytest.fixture
def snowflake_configuration():
    return SnowClientConfig(
        account="test_account",
        user="test_user",
        password="test_password",
        database="test_db",
    )


@pytest.fixture
def snowflake_client(snowflake_configuration):
    client = SnowClient(snowflake_configuration)
    client.connection = MagicMock()
    return client


@pytest.fixture
def policy_validation_service(policy_config_service):
    return PolicyValidationService(policy_config_service)


@pytest.mark.parametrize(
    "assignments, expected_error",
    [
        (
            {
                "column_masking_policies": {"MP_1": {}, "MP_2": {}},
                "row_access_policies": {"RAP_1": {}, "RAP_2": {}},
            },
            None,
        ),
        (
            {
                "column_masking_policies": {"MP_1": {}, "MY_MASKING_POLICY": {}},
                "row_access_policies": {"RAP_1": {}, "RAP_2": {}},
            },
            None,
        ),
        (
            {
                "column_masking_policies": {"invalid_mp": {}, "MP_2": {}},
                "row_access_policies": {"RAP_1": {}, "RAP_2": {}},
            },
            "Column masking policy invalid_mp in project test_project does not follow the naming convention with regex ^MP_.*$|MY_MASKING_POLICY",
        ),
        (
            {
                "column_masking_policies": {"MP_1": {}, "MP_2": {}},
                "row_access_policies": {"invalid_rap": {}, "RAP_2": {}},
            },
            "Row access policy invalid_rap in project test_project does not follow the naming convention with regex ^RAP_.*$",
        ),
    ],
)
def test_validate_naming_conventions(
    policy_validation_service, assignments, expected_error
):
    project = "test_project"
    if expected_error:
        try:
            policy_validation_service._validate_naming_conventions(project, assignments)
        except ValueError as e:
            assert str(e) == expected_error
        else:
            assert False, f"Expected ValueError: {expected_error}"
    else:
        assert (
            policy_validation_service._validate_naming_conventions(project, assignments)
            is None
        )


@pytest.mark.parametrize(
    "assignments, expected_error",
    [
        (
            {
                "row_access_policies": {
                    "RAP_TEST": {
                        "annotations": {},
                        "tables": {"schema1.table1": ["column1"]},
                        "views": {},
                    },
                    "RAP_TEST_2": {"annotations": {}, "tables": {}, "views": {}},
                }
            },
            None,
        ),
        (
            {
                "row_access_policies": {
                    "RAP_TEST": {
                        "annotations": {},
                        "tables": {"schema1.table1": ["column1"]},
                        "views": {},
                    },
                    "RAP_TEST_2": {
                        "annotations": {},
                        "tables": {
                            "schema1.table2": [],
                        },
                        "views": {},
                    },
                }
            },
            "Row access policy RAP_TEST_2 assignment (of type 'tables') on schema1.table2 in project test_project does not have at least one argument column defined.",
        ),
    ],
)
def test_validate_at_least_one_argument_column_rap(
    policy_validation_service, assignments, expected_error
):
    project = "test_project"
    if expected_error:
        try:
            policy_validation_service._validate_at_least_one_argument_column_rap(
                project, assignments
            )
        except ValueError as e:
            assert str(e) == expected_error
        else:
            assert False, f"Expected ValueError: {expected_error}"
    else:
        assert (
            policy_validation_service._validate_at_least_one_argument_column_rap(
                project, assignments
            )
            is None
        )


@pytest.mark.parametrize(
    "assignments_transposed, expected_error",
    [
        (
            {
                "column_masking_policies": {
                    "table_columns": {
                        "table1.column1": ["CMP_1"],
                        "table1.column2": ["CMP_2", "CMP_3"],
                        "table2.column1": ["CMP_1"],
                    },
                    "view_columns": {
                        "view1.column1": ["CMP_2"],
                        "view1.column2": ["CMP_3"],
                        "view2.column1": ["CMP_1"],
                    },
                    "dynamictable_columns": {},
                },
                "row_access_policies": {
                    "tables": {
                        "table1": ["RAP_1"],
                        "table2": ["RAP_2"],
                    },
                    "views": {
                        "view1": ["RAP_1"],
                        "view2": ["RAP_2"],
                    },
                    "dynamictables": {},
                },
            },
            "There are multiple MASKING POLICY assignments defined for table column TABLE1.COLUMN2 in project test_project! List of assigned column_masking_policies: ['CMP_2', 'CMP_3']!",
        ),
        (
            {
                "column_masking_policies": {
                    "table_columns": {
                        "table1.column1": ["CMP_1"],
                        "table1.column2": ["CMP_2"],
                        "table2.column1": ["CMP_1"],
                    },
                    "view_columns": {
                        "view1.column1": ["CMP_2", "CMP_3"],
                        "view1.column2": ["CMP_3"],
                        "view2.column1": ["CMP_1"],
                    },
                    "dynamictable_columns": {},
                },
                "row_access_policies": {
                    "tables": {
                        "table1": ["RAP_1"],
                        "table2": ["RAP_2"],
                    },
                    "views": {
                        "view1": ["RAP_1"],
                        "view2": ["RAP_2"],
                    },
                    "dynamictables": {},
                },
            },
            "There are multiple MASKING POLICY assignments defined for view column VIEW1.COLUMN1 in project test_project! List of assigned column_masking_policies: ['CMP_2', 'CMP_3']!",
        ),
        (
            {
                "column_masking_policies": {
                    "table_columns": {
                        "table1.column1": ["CMP_1"],
                        "table1.column2": ["CMP_2"],
                        "table2.column1": ["CMP_1"],
                    },
                    "view_columns": {
                        "view1.column1": ["CMP_2"],
                        "view1.column2": ["CMP_3"],
                        "view2.column1": ["CMP_1"],
                    },
                    "dynamictable_columns": {},
                },
                "row_access_policies": {
                    "tables": {
                        "table1": ["RAP_1"],
                        "table2": ["RAP_2", "RAP_3", "RAP_4"],
                    },
                    "views": {
                        "view1": ["RAP_1"],
                        "view2": ["RAP_2"],
                    },
                    "dynamictables": {},
                },
            },
            "There are multiple ROW ACCESS POLICY assignments defined for table TABLE2 in project test_project! List of assigned row_access_policies: ['RAP_2', 'RAP_3', 'RAP_4']!",
        ),
        (
            {
                "column_masking_policies": {
                    "table_columns": {
                        "table1.column1": ["CMP_1"],
                        "table1.column2": ["CMP_2"],
                        "table2.column1": ["CMP_1"],
                    },
                    "view_columns": {
                        "view1.column1": ["CMP_2"],
                        "view1.column2": ["CMP_3"],
                        "view2.column1": ["CMP_1"],
                    },
                    "dynamictable_columns": {},
                },
                "row_access_policies": {
                    "tables": {
                        "table1": ["RAP_1"],
                        "table2": ["RAP_2"],
                    },
                    "views": {
                        "view1": ["RAP_1"],
                        "view2": ["RAP_2", "RAP_3"],
                    },
                    "dynamictables": {},
                },
            },
            "There are multiple ROW ACCESS POLICY assignments defined for view VIEW2 in project test_project! List of assigned row_access_policies: ['RAP_2', 'RAP_3']!",
        ),
        (
            {
                "column_masking_policies": {
                    "table_columns": {
                        "table1.column1": ["CMP_1"],
                        "table1.column2": ["CMP_2"],
                        "table2.column1": ["CMP_1"],
                    },
                    "view_columns": {
                        "view1.column1": ["CMP_2"],
                        "view1.column2": ["CMP_3"],
                        "view2.column1": ["CMP_1"],
                    },
                    "dynamictable_columns": {},
                },
                "row_access_policies": {
                    "tables": {
                        "table1": ["RAP_1"],
                        "table2": ["RAP_2"],
                    },
                    "views": {
                        "view1": ["RAP_1"],
                        "view2": ["RAP_2"],
                    },
                    "dynamictables": {},
                },
            },
            None,
        ),
    ],
)
def test_validate_policy_assignment_uniqueness(
    policy_validation_service, assignments_transposed, expected_error
):
    project = "test_project"
    if expected_error:
        try:
            policy_validation_service._validate_policy_assignment_uniqueness(
                project, assignments_transposed
            )
        except ValueError as e:
            assert str(e) == expected_error
        else:
            assert False, f"Expected ValueError: {expected_error}"
    else:
        assert (
            policy_validation_service._validate_policy_assignment_uniqueness(
                project, assignments_transposed
            )
            is None
        )


@pytest.mark.parametrize(
    "policy_identifier, policy_type,policy_type_as_sql_string, policy_assignment ,argument_columns, policy_signature, expected_error",
    [
        (
            "TEST_DB.TEST_SCHEMA.CMP_1",
            PolicyType.COLUMN_MASKING_POLICY,
            "MASKING POLICY",
            "TABLE1.COLUMN1",
            ["arg1", "arg2"],
            {0: "VARCHAR", 1: "NUMBER", 2: "NUMBER"},
            None,
        ),
        (
            "TEST_DB.TEST_SCHEMA.CMP_1",
            PolicyType.COLUMN_MASKING_POLICY,
            "MASKING POLICY",
            "TABLE1.COLUMN1",
            ["arg1"],
            {0: "VARCHAR", 1: "NUMBER", 2: "NUMBER"},
            """
            The number of argument columns 1 for the assignment of MASKING POLICY TEST_DB.TEST_SCHEMA.CMP_1 on TABLE1.COLUMN1
            in project test_project does not match the number of argument columns 2 in the policy signature!
            """,
        ),
        (
            "TEST_DB.TEST_SCHEMA.CMP_2",
            PolicyType.COLUMN_MASKING_POLICY,
            "MASKING POLICY",
            "TABLE2.COLUMN1",
            ["arg1", "arg2", "arg3"],
            {0: "VARCHAR", 1: "NUMBER", 2: "NUMBER"},
            """
            The number of argument columns 3 for the assignment of MASKING POLICY TEST_DB.TEST_SCHEMA.CMP_2 on TABLE2.COLUMN1
            in project test_project does not match the number of argument columns 2 in the policy signature!
            """,
        ),
        (
            "TEST_DB.TEST_SCHEMA.RAP_1",
            PolicyType.ROW_ACCESS_POLICY,
            "ROW ACCESS POLICY",
            "VIEW2.COLUMN1",
            ["arg1", "arg2"],
            {0: "VARCHAR", 1: "NUMBER", 2: "NUMBER"},
            """
            The number of argument columns 2 for the assignment of ROW ACCESS POLICY TEST_DB.TEST_SCHEMA.RAP_1 on VIEW2.COLUMN1
            in project test_project does not match the number of argument columns 3 in the policy signature!
            """,
        ),
    ],
)
def test_number_of_assignment_columns(
    policy_validation_service,
    policy_identifier,
    policy_type,
    policy_type_as_sql_string,
    policy_assignment,
    argument_columns,
    policy_signature,
    expected_error,
):
    project = "test_project"

    if expected_error is not None:
        try:
            policy_validation_service._validate_number_of_assignment_columns(
                project,
                policy_identifier,
                policy_type,
                policy_type_as_sql_string,
                policy_assignment,
                argument_columns,
                policy_signature,
            )
        except ValueError as e:
            assert str(e).replace(" ", "") == expected_error.replace(" ", "")
    else:
        policy_validation_service._validate_number_of_assignment_columns(
            project,
            policy_identifier,
            policy_type,
            policy_type_as_sql_string,
            policy_assignment,
            argument_columns,
            policy_signature,
        )
