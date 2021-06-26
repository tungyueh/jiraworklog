from operator import attrgetter
from typing import List

from jiraworklog.issue import IssueInterface, Issue, IssueInSprint
from jiraworklog.jira import Jira
from jiraworklog.sprint import Sprint

SECONDS_IN_HOUR = 3600


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
