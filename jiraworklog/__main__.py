import argparse
from typing import List

from jiraworklog.issue import Issue
from jiraworklog.jira import make_jira


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
        if issue.time_spent_in_second:
            total_seconds += issue.time_spent_in_second
    return total_seconds


if __name__ == '__main__':
    main()
