import argparse
from typing import List

from jiraworklog.issue import Issue
from jiraworklog.jira import make_jira


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('server_url', help='Server URL')
    parser.add_argument('jql', help='Jira Query Language')
    parser.add_argument('-b', dest='board_id', help='Board ID')

    args = parser.parse_args()

    jira = make_jira(args.server_url)
    issues = jira.search_issues(args.jql)
    if args.board_id:
        sprint = jira.active_sprint(args.board_id)
        if not sprint:
            print('No active sprint')
            return
        total_seconds = time_spent_in_sprint(issues, jira, sprint)
    else:
        total_seconds = total_time_spent(issues)
    print(f'Total time spent: {total_seconds / 3600} hour')


def time_spent_in_sprint(issues, jira, sprint):
    total_seconds = 0
    for issue in issues:
        total_seconds += issue_time_spent_in_sprint(issue, jira, sprint)
    return total_seconds


def issue_time_spent_in_sprint(issue, jira, sprint):
    total_seconds = 0
    for work_log in jira.work_logs(issue):
        if is_work_log_in_sprint(sprint, work_log):
            total_seconds += work_log.time_spent_in_seconds
    return total_seconds


def is_work_log_in_sprint(sprint, work_log):
    return sprint.start_time <= work_log.logged_time <= sprint.end_time


def total_time_spent(issues: List[Issue]) -> int:
    total_seconds = 0
    for issue in issues:
        if issue.time_spent_in_second:
            total_seconds += issue.time_spent_in_second
    return total_seconds


if __name__ == '__main__':
    main()
