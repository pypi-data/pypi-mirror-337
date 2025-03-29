import pytest

from policy_tool.services.policy_solution_service import PolicySolutionClient


@pytest.mark.parametrize(
    "project, expected_all_policy_assignments, expected_all_policy_assignments_transposed",
    [
        (
            "PROJECT1",
            {
                "column_masking_policies": {
                    "MP_CONDITIONAL_TEST": {
                        "table_columns": {},
                        "view_columns": {},
                        "tags": [],
                        "dynamictable_columns": {},
                    },
                    "MP_CONDITIONAL_TEST_2": {
                        "table_columns": {"TEST_DATA.REGIONS.COUNTRY": ["REGION_ID"]},
                        "view_columns": {"TEST_DATA.V_REGIONS.COUNTRY": ["REGION_ID"]},
                        "tags": [],
                        "dynamictable_columns": {},
                    },
                    "MP_COUNTRY_MASK": {
                        "table_columns": {"TEST_DATA.SALES_DATA.NOT_EXISTING": []},
                        "view_columns": {"TEST_DATA.V_NOT_EXISTING.COUNTRY": []},
                        "tags": [
                            "POLICIES.TAG_SALES_ACCESS",
                            "POLICIES.TAG_COSTUMER_ACCESS",
                        ],
                        "dynamictable_columns": {},
                    },
                    "MP_PRICE_MASK": {
                        "table_columns": {},
                        "view_columns": {},
                        "tags": [
                            "POLICIES.TAG_SALES_ACCESS",
                            "POLICIES.TAG_NOT_EXISTING",
                        ],
                        "dynamictable_columns": {},
                    },
                },
                "row_access_policies": {
                    "RAP_TEST": {
                        "tables": {"TEST_DATA.REGIONS": ["REGION_ID"]},
                        "views": {},
                        "dynamictables": {},
                    },
                    "RAP_TEST_2": {"tables": {}, "views": {}, "dynamictables": {}},
                },
            },
            {
                "column_masking_policies": {
                    "table_columns": {
                        "TEST_DATA.REGIONS.COUNTRY": ["MP_CONDITIONAL_TEST_2"],
                        "TEST_DATA.SALES_DATA.NOT_EXISTING": ["MP_COUNTRY_MASK"],
                    },
                    "view_columns": {
                        "TEST_DATA.V_REGIONS.COUNTRY": ["MP_CONDITIONAL_TEST_2"],
                        "TEST_DATA.V_NOT_EXISTING.COUNTRY": ["MP_COUNTRY_MASK"],
                    },
                    "tags": {
                        "POLICIES.TAG_SALES_ACCESS": [
                            "MP_COUNTRY_MASK",
                            "MP_PRICE_MASK",
                        ],
                        "POLICIES.TAG_COSTUMER_ACCESS": ["MP_COUNTRY_MASK"],
                        "POLICIES.TAG_NOT_EXISTING": ["MP_PRICE_MASK"],
                    },
                    "dynamictable_columns": {},
                },
                "row_access_policies": {
                    "tables": {"TEST_DATA.REGIONS": ["RAP_TEST"]},
                    "views": {},
                    "dynamictables": {},
                },
                "schemas": ["TEST_DATA", "POLICIES"],
            },
        )
    ],
)
def test_load_policy_assignments_from_files(
    project,
    expected_all_policy_assignments,
    expected_all_policy_assignments_transposed,
):
    policy_assignments_files = {
        project: ["tests/policy_tool/services/policy_assignments_json_fixture.json"]
    }

    policy_solution_client = PolicySolutionClient(policy_assignments_files)

    assert policy_solution_client.all_policy_assignments == {
        project: expected_all_policy_assignments
    }
    assert policy_solution_client.all_policy_assignments_transposed == {
        project: expected_all_policy_assignments_transposed
    }
