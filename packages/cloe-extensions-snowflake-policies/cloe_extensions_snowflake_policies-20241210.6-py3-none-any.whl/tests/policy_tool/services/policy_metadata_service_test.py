from unittest.mock import MagicMock

import pytest

from policy_tool.services.policy_metadata_service import PolicyMetadataService
from policy_tool.services.snowflake_service import SnowClient, SnowClientConfig


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


@pytest.mark.parametrize(
    "cmp_references, rap_references, expected_all_policy_assignments, expected_all_policy_assignments_transposed",
    [
        (
            [
                {
                    "POLICY_DB": "PROJECT1_DEVELOPMENT",
                    "POLICY_SCHEMA": "POLICIES",
                    "POLICY_NAME": "MP_CONDITIONAL_TEST_2",
                    "POLICY_KIND": "MASKING_POLICY",
                    "REF_DATABASE_NAME": "PROJECT1_DEVELOPMENT",
                    "REF_SCHEMA_NAME": "TEST_DATA",
                    "REF_ENTITY_NAME": "REGIONS",
                    "REF_ENTITY_DOMAIN": "TABLE",
                    "REF_COLUMN_NAME": "COUNTRY",
                    "REF_ARG_COLUMN_NAMES": '[ "REGION_ID" ]',
                    "TAG_DATABASE": None,
                    "TAG_SCHEMA": None,
                    "TAG_NAME": None,
                    "POLICY_STATUS": "ACTIVE",
                },
                {
                    "POLICY_DB": "PROJECT1_DEVELOPMENT",
                    "POLICY_SCHEMA": "POLICIES",
                    "POLICY_NAME": "MP_CONDITIONAL_TEST_2",
                    "POLICY_KIND": "MASKING_POLICY",
                    "REF_DATABASE_NAME": "PROJECT1_DEVELOPMENT",
                    "REF_SCHEMA_NAME": "TEST_DATA",
                    "REF_ENTITY_NAME": "V_REGIONS",
                    "REF_ENTITY_DOMAIN": "VIEW",
                    "REF_COLUMN_NAME": "COUNTRY",
                    "REF_ARG_COLUMN_NAMES": '[ "REGION_ID" ]',
                    "TAG_DATABASE": None,
                    "TAG_SCHEMA": None,
                    "TAG_NAME": None,
                    "POLICY_STATUS": "ACTIVE",
                },
                {
                    "POLICY_DB": "PROJECT1_DEVELOPMENT",
                    "POLICY_SCHEMA": "POLICIES",
                    "POLICY_NAME": "MP_COUNTRY_MASK",
                    "POLICY_KIND": "MASKING_POLICY",
                    "REF_DATABASE_NAME": "PROJECT1_DEVELOPMENT",
                    "REF_SCHEMA_NAME": "POLICIES",
                    "REF_ENTITY_NAME": "TAG_COSTUMER_ACCESS",
                    "REF_ENTITY_DOMAIN": "TAG",
                    "REF_COLUMN_NAME": None,
                    "REF_ARG_COLUMN_NAMES": None,
                    "TAG_DATABASE": None,
                    "TAG_SCHEMA": None,
                    "TAG_NAME": None,
                    "POLICY_STATUS": "ACTIVE",
                },
                {
                    "POLICY_DB": "PROJECT1_DEVELOPMENT",
                    "POLICY_SCHEMA": "POLICIES",
                    "POLICY_NAME": "MP_COUNTRY_MASK",
                    "POLICY_KIND": "MASKING_POLICY",
                    "REF_DATABASE_NAME": "PROJECT1_DEVELOPMENT",
                    "REF_SCHEMA_NAME": "POLICIES",
                    "REF_ENTITY_NAME": "TAG_SALES_ACCESS",
                    "REF_ENTITY_DOMAIN": "TAG",
                    "REF_COLUMN_NAME": None,
                    "REF_ARG_COLUMN_NAMES": None,
                    "TAG_DATABASE": None,
                    "TAG_SCHEMA": None,
                    "TAG_NAME": None,
                    "POLICY_STATUS": "ACTIVE",
                },
                {
                    "POLICY_DB": "PROJECT1_DEVELOPMENT",
                    "POLICY_SCHEMA": "POLICIES",
                    "POLICY_NAME": "MP_PRICE_MASK",
                    "POLICY_KIND": "MASKING_POLICY",
                    "REF_DATABASE_NAME": "PROJECT1_DEVELOPMENT",
                    "REF_SCHEMA_NAME": "POLICIES",
                    "REF_ENTITY_NAME": "TAG_SALES_ACCESS",
                    "REF_ENTITY_DOMAIN": "TAG",
                    "REF_COLUMN_NAME": None,
                    "REF_ARG_COLUMN_NAMES": None,
                    "TAG_DATABASE": None,
                    "TAG_SCHEMA": None,
                    "TAG_NAME": None,
                    "POLICY_STATUS": "ACTIVE",
                },
            ],
            [
                {
                    "POLICY_DB": "PROJECT1_DEVELOPMENT",
                    "POLICY_SCHEMA": "POLICIES",
                    "POLICY_NAME": "RAP_TEST",
                    "POLICY_KIND": "ROW_ACCESS_POLICY",
                    "REF_DATABASE_NAME": "PROJECT1_DEVELOPMENT",
                    "REF_SCHEMA_NAME": "TEST_DATA",
                    "REF_ENTITY_NAME": "REGIONS",
                    "REF_ENTITY_DOMAIN": "TABLE",
                    "REF_COLUMN_NAME": None,
                    "REF_ARG_COLUMN_NAMES": '[ "REGION_ID" ]',
                    "TAG_DATABASE": None,
                    "TAG_SCHEMA": None,
                    "TAG_NAME": None,
                    "POLICY_STATUS": "ACTIVE",
                }
            ],
            {
                "column_masking_policies": {
                    "MP_CONDITIONAL_TEST_2": {
                        "annotations": {},
                        "table_columns": {"TEST_DATA.REGIONS.COUNTRY": ["REGION_ID"]},
                        "view_columns": {"TEST_DATA.V_REGIONS.COUNTRY": ["REGION_ID"]},
                        "tags": [],
                        "dynamictable_columns": {},
                    },
                    "MP_COUNTRY_MASK": {
                        "annotations": {},
                        "table_columns": {},
                        "view_columns": {},
                        "tags": [
                            "POLICIES.TAG_COSTUMER_ACCESS",
                            "POLICIES.TAG_SALES_ACCESS",
                        ],
                        "dynamictable_columns": {},
                    },
                    "MP_PRICE_MASK": {
                        "annotations": {},
                        "table_columns": {},
                        "view_columns": {},
                        "tags": ["POLICIES.TAG_SALES_ACCESS"],
                        "dynamictable_columns": {},
                    },
                },
                "row_access_policies": {
                    "RAP_TEST": {
                        "annotations": {},
                        "tables": {"TEST_DATA.REGIONS": ["REGION_ID"]},
                        "views": {},
                        "dynamictables": {},
                    }
                },
            },
            {
                "column_masking_policies": {
                    "table_columns": {
                        "TEST_DATA.REGIONS.COUNTRY": "MP_CONDITIONAL_TEST_2"
                    },
                    "view_columns": {
                        "TEST_DATA.V_REGIONS.COUNTRY": "MP_CONDITIONAL_TEST_2"
                    },
                    "tags": {
                        "POLICIES.TAG_COSTUMER_ACCESS": ["MP_COUNTRY_MASK"],
                        "POLICIES.TAG_SALES_ACCESS": [
                            "MP_COUNTRY_MASK",
                            "MP_PRICE_MASK",
                        ],
                    },
                    "dynamictable_columns": {},
                },
                "row_access_policies": {
                    "tables": {"TEST_DATA.REGIONS": "RAP_TEST"},
                    "views": {},
                    "dynamictables": {},
                },
            },
        )
    ],
)
def test_parse_cmp_rap_references(
    snowflake_client,
    cmp_references,
    rap_references,
    expected_all_policy_assignments,
    expected_all_policy_assignments_transposed,
):
    database = "PROJECT1_DEVELOPMENT"

    policy_metadata_service = PolicyMetadataService(snowflake_client, database)

    policy_metadata_service._parse_cmp_rap_references(cmp_references, rap_references)

    assert policy_metadata_service.policy_assignments == expected_all_policy_assignments

    assert (
        policy_metadata_service.policy_assignments_transposed
        == expected_all_policy_assignments_transposed
    )
