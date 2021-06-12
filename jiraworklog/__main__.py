import argparse

from jiraworklog.issues_worklog import IssuesWorkLog
from jiraworklog.jira import make_jira


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('server_url', help='Server URL')
    parser.add_argument('jql', help='Jira Query Language')
    parser.add_argument('-b', dest='board_id', help='Board ID')
    parser.add_argument('-s', dest='sprint_id', help='Sprint ID')

    args = parser.parse_args()

    jira = make_jira(args.server_url)
    issues = jira.search_issues(args.jql)
    if args.board_id:
        sprint = jira.active_sprint(args.board_id)
        if not sprint:
            print('No active sprint')
            return
        total_seconds = time_spent_in_sprint(issues, jira, sprint)
    elif args.sprint_id:
        sprint = jira.get_sprint(args.sprint_id)
        total_seconds = time_spent_in_sprint(issues, jira, sprint)
    else:
        total_seconds = IssuesWorkLog(issues).compute()
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
    return sprint.start_time <= work_log.logged_time <= (sprint.end_time+86400)


if __name__ == '__main__':
    main()
