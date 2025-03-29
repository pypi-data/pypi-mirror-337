import os

#########################################################################################
#########################################################################################


def load_snowflake_credentials(config: dict, project: str, environment: int) -> dict:
    snowflake_params = {
        "account": config["SNOWFLAKE_ACCOUNT"],
        "warehouse": config["SNOWFLAKE_WAREHOUSE"],
        "user": config["PROJECT_CONFIGS"][project]["SNOWFLAKE_CREDENTIALS"]["USER"],
        "password": os.getenv(
            config["PROJECT_CONFIGS"][project]["SNOWFLAKE_CREDENTIALS"]["PASSWORD_NAME"]
        ),
        "role": config["PROJECT_CONFIGS"][project]["SNOWFLAKE_CREDENTIALS"]["ROLE"],
        "database": config["PROJECT_CONFIGS"][project]["ENVIRONMENTS"][environment],
    }

    return snowflake_params
