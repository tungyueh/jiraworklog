import argparse
import getpass
from typing import List

from requests.utils import get_netrc_auth
from jira import JIRA, Issue

URL = str


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('server_url', help='Server URL')
    parser.add_argument('jql', help='Jira Query Language')
    args = parser.parse_args()

    jira = make_jira(args.server_url)
    issues = jira.search_issues(args.jql)
    total_seconds = total_time_spent(issues)
    print(f'Total time spent: {total_seconds / 3600} hour')


def total_time_spent(issues: List[Issue]) -> int:
    total_seconds = 0
    for issue in issues:
        if issue.fields.timespent:
            total_seconds += issue.fields.timespent
    return total_seconds


def make_jira(jira_server: URL) -> JIRA:
    if not get_netrc_auth(jira_server):
        user = input("Jira Username:")
        password = getpass.getpass()
        jira = JIRA(jira_server, basic_auth=(user, password))
    else:
        jira = JIRA(jira_server)
    return jira


if __name__ == '__main__':
    main()
