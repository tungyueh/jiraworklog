import argparse

from jiraworklog.issues_worklog import IssuesWorkLog
from jiraworklog.jira import make_jira
from jiraworklog.sprint_worklog import SprintWorkLogs


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
        total_seconds = SprintWorkLogs(jira, sprint, issues).compute()
    elif args.sprint_id:
        sprint = jira.get_sprint(args.sprint_id)
        total_seconds = SprintWorkLogs(jira, sprint, issues).compute()
    else:
        total_seconds = IssuesWorkLog(issues).compute()
    print(f'Total time spent: {total_seconds / 3600} hour')


if __name__ == '__main__':
    main()
