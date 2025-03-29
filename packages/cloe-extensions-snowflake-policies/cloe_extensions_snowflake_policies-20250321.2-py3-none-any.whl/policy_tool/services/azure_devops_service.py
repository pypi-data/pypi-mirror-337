import base64
import json
import logging

import requests

from policy_tool.services.policy_configuration_service import PolicyConfigService
from policy_tool.utils.logger_utils import LoggingAdapter

logger = logging.getLogger(__name__)
log = LoggingAdapter(logger)


def create_pr_comment(comment_markdown: str, policy_config: PolicyConfigService):
    authorization = str(
        base64.b64encode(bytes(":" + policy_config.system_accesstoken, "ascii")),
        "ascii",
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + authorization,
    }

    data = {
        "comments": [
            {"parentCommentId": 0, "content": comment_markdown, "commentType": 1}
        ],
        "status": 1,
    }

    url = f"{policy_config.system_teamfoundationcollectionuri}{policy_config.system_teamprojectid}/_apis/git/repositories/{policy_config.build_repository_name}/pullRequests/{policy_config.system_pullrequest_pullrequestid}/threads?api-version=7.0"

    response = requests.post(url=url, headers=headers, verify=True, json=data)

    if response.status_code == 200:
        api_response = json.loads(response.text)
        return api_response, True
    else:
        log.info(f"request url: {url}")
        log.info(f"request response.status_code: {response.status_code}")
        log.info(f"request response.text: {response.text}")
        raise EnvironmentError(
            f"Error while trying to create a comment on pull request {policy_config.system_pullrequest_pullrequestid} - Pull Request Threads Rest API!"
        )


def parse_comment_policy_assignments_to_be_ignored(
    policy_assignments_to_be_ignored: dict, project: str, database: str
) -> str:
    comment_markdown_policy_assignments_to_be_ignored = ""

    if policy_assignments_to_be_ignored:
        comment_markdown_policy_assignments_to_be_ignored = f'## <span style="color:lightgreen">OVERVIEW: Ignored Policy Assignments</span> \n The following objects do not yet exist on the database {database} in project {project}.\n Policy assignments are consequently ignored until the objects are deployed on the database. \n'

        for object_type in policy_assignments_to_be_ignored.keys():
            ignored_policy_assignments = policy_assignments_to_be_ignored[object_type]

            table = "| Object Identifier | Assignment Object Identifier | Policy Assignment | Policy Assignment Type |\n"
            table += "| --- | --- | --- | --- |\n"

            for ignored_policy_assignment in ignored_policy_assignments:
                object_identifier = ignored_policy_assignment["object_identifier"]
                assignment_object_identifier = ignored_policy_assignment[
                    "assignment_object_identifier"
                ]
                policy_assignment = ignored_policy_assignment["policy_assignment"]
                policy_assignment_type = ignored_policy_assignment[
                    "policy_assignment_type"
                ]

                row = f"| {object_identifier} | {assignment_object_identifier} | {policy_assignment} | {policy_assignment_type} |\n"

                table += row

            comment_markdown_policy_assignments_to_be_ignored += (
                f"## {object_type}\n\n{table}"
            )

    return comment_markdown_policy_assignments_to_be_ignored


def parse_comment_warning_removal_policy_assignments(
    warning_removal_of_policy_assignment: bool = False,
):
    comment_warning_removal_policy_assignments = ""

    if warning_removal_of_policy_assignment:
        comment_warning_removal_policy_assignments = '## <span style="color:orange">WARNING: REMOVAL OF POLICY ASSIGNMENTS DETECTED</span> \n The dry-run produced sql-statements that lead to the removal of policy assignments. Please review the sql-statements and the assignment-files before approving the Pull Request! \n Note: The sql-statements can be found in the pipeline artifacts, in the pipeline log and in the policy_assignments_history. \n\n'

    return comment_warning_removal_policy_assignments
