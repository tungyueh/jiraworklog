import argparse
import time
from typing import List

from jiraworklog.issue import Issue, IssueInterface, IssueInSprint
from jiraworklog.jira import make_jira, Jira
from jiraworklog.sprint import Sprint


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('server_url', help='Server URL')
    parser.add_argument('jql', help='Jira Query Language')
    parser.add_argument('-b', dest='board_id', help='Board ID')
    parser.add_argument('-s', dest='sprint_id', help='Sprint ID')

    args = parser.parse_args()

    jira = make_jira(args.server_url)
    start_time = time.time()
    print(f'Start search issues... "{args.jql}"')
    issues = jira.search_issues(args.jql)
    search_time = time.time() - start_time
    print(f'Search issues done. Spent time: {search_time} seconds')
    if args.board_id:
        sprint = jira.active_sprint(args.board_id)
        if not sprint:
            print('No active sprint')
            return
        time_spent_issues = make_issues_in_sprint(jira, sprint, issues)
    elif args.sprint_id:
        sprint = jira.get_sprint(args.sprint_id)
        time_spent_issues = make_issues_in_sprint(jira, sprint, issues)
    else:
        time_spent_issues = issues
    total_seconds = sum([i.time_spent_in_second for i in time_spent_issues])
    print(f'Total time spent: {total_seconds / 3600} hour')


def make_issues_in_sprint(jira: Jira, sprint: Sprint, issues: List[Issue]) -> \
        List[IssueInterface]:
    issues_in_sprint: List[IssueInterface] = []
    for issue in issues:
        work_logs = jira.work_logs(issue)
        issues_in_sprint.append(IssueInSprint(sprint, work_logs))
    return issues_in_sprint


if __name__ == '__main__':
    main()
