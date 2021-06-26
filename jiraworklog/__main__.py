import argparse
import time
from operator import attrgetter
from typing import List

from jiraworklog.issue import Issue, IssueInterface, IssueInSprint
from jiraworklog.jira import make_jira, Jira
from jiraworklog.sprint import Sprint

SECONDS_IN_HOUR = 3600


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('server_url', help='Server URL')
    parser.add_argument('jql', help='Jira Query Language')
    parser.add_argument('-b', dest='board_id', help='Board ID')
    parser.add_argument('-s', dest='sprint_id', help='Sprint ID')
    parser.add_argument('--duration', dest='num_most_time_spend_issues',
                        type=int,
                        help='Show N most time spent issues (N=0 for all)')

    args = parser.parse_args()

    jira = make_jira(args.server_url)
    start_time = time.time()
    print(f'Start search issues... "{args.jql}"')
    issues = jira.search_issues(args.jql)
    search_time = time.time() - start_time
    print(f'Search issues done. Find: {len(issues)} issues, '
          f'Spent time: {search_time} seconds')
    time_spent_issues = make_time_spent_issues(args.board_id, issues, jira,
                                               args.sprint_id)
    show_total_time_spent(time_spent_issues)
    if args.num_most_time_spend_issues is not None:
        show_all_issues = args.num_most_time_spend_issues == 0
        if show_all_issues:
            show_all_time_spent_issues(time_spent_issues)
        else:
            show_most_time_spent_issues(time_spent_issues,
                                        args.num_most_time_spend_issues)


def make_time_spent_issues(board_id, issues, jira, sprint_id) -> \
        List[IssueInterface]:
    if board_id:
        sprint = jira.active_sprint(board_id)
        if not sprint:
            print('No active sprint')
            time_spent_issues = []
        else:
            time_spent_issues = make_issues_in_sprint(jira, sprint, issues)
    elif sprint_id:
        sprint = jira.get_sprint(sprint_id)
        time_spent_issues = make_issues_in_sprint(jira, sprint, issues)
    else:
        time_spent_issues = issues
    return time_spent_issues


def show_total_time_spent(time_spent_issues):
    total_seconds = sum([i.time_spent_in_second for i in time_spent_issues])
    print(f'Total time spent: {total_seconds / SECONDS_IN_HOUR} hour')


def show_all_time_spent_issues(time_spent_issues: List[IssueInterface]):
    issues = sort_issue_by_time_spent(time_spent_issues)
    for issue in issues:
        print(make_issue_summary(issue))


def sort_issue_by_time_spent(time_spent_issues: List[IssueInterface]):
    issues = sorted(time_spent_issues, key=attrgetter('time_spent_in_second'),
                    reverse=True)
    return issues


def make_issue_summary(issue):
    return f'{issue.key} {issue.assignee:12} ' \
           f'{issue.time_spent_in_second / SECONDS_IN_HOUR:.2f}h ' \
           f'{issue.summary}'


def show_most_time_spent_issues(time_spent_issues: List[IssueInterface],
                                num_most_time_spend_issues: int):
    issues = sort_issue_by_time_spent(time_spent_issues)
    for issue in issues[:num_most_time_spend_issues]:
        print(make_issue_summary(issue))


def make_issues_in_sprint(jira: Jira, sprint: Sprint, issues: List[Issue]) -> \
        List[IssueInterface]:
    issues_in_sprint: List[IssueInterface] = []
    for issue in issues:
        work_logs = jira.work_logs(issue)
        issues_in_sprint.append(IssueInSprint(issue, sprint, work_logs))
    return issues_in_sprint


if __name__ == '__main__':
    main()
