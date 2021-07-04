from collections import defaultdict
from operator import attrgetter
from typing import List, Dict

from jiraworklog.issue import IssueInterface, Issue, IssueInSprint
from jiraworklog.jira import Jira
from jiraworklog.sprint import Sprint

SECONDS_IN_MINUTE = 60
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


def show_total_time_spent(issues: List[IssueInterface]):
    total_seconds = sum_time_spent_in_seconds(issues)
    print(make_total_time_spent_message(total_seconds))


def sum_time_spent_in_seconds(issues: List[IssueInterface]) -> int:
    return sum([i.time_spent_in_second for i in issues])


def make_total_time_spent_message(total_seconds: int) -> str:
    return f'Total time spent: {total_seconds / SECONDS_IN_HOUR:.2f} hours'


def show_total_time_spent_by_assignee(issues: List[IssueInterface]):
    assignee_time_spent: Dict[str, int] = defaultdict(int)
    for issue in issues:
        if issue.time_spent_in_second == 0:
            continue
        assignee_time_spent[issue.assignee] += issue.time_spent_in_second
    for assignee, total_seconds in assignee_time_spent.items():
        total_time_spent_msg = make_total_time_spent_message(total_seconds)
        print(f'{assignee:12} {total_time_spent_msg}')


def show_all_time_spent_issues(time_spent_issues: List[IssueInterface]):
    issues = sort_issue_by_time_spent(time_spent_issues)
    for issue in issues:
        if issue.time_spent_in_second:
            print(make_issue_summary(issue))


def sort_issue_by_time_spent(time_spent_issues: List[IssueInterface]):
    issues = sorted(time_spent_issues, key=attrgetter('time_spent_in_second'),
                    reverse=True)
    return issues


def make_issue_summary(issue):
    return f'{issue.key} {issue.assignee:12} ' \
           f'{make_hh_mm(issue.time_spent_in_second)} ' \
           f'{issue.summary}'


def show_most_time_spent_issues(time_spent_issues: List[IssueInterface],
                                num_most_time_spend_issues: int):
    issues = sort_issue_by_time_spent(time_spent_issues)
    for issue in issues[:num_most_time_spend_issues]:
        if issue.time_spent_in_second:
            print(make_issue_summary(issue))


def make_issues_in_sprint(jira: Jira, sprint: Sprint, issues: List[Issue]) -> \
        List[IssueInterface]:
    issues_in_sprint: List[IssueInterface] = []
    for issue in issues:
        work_logs = jira.work_logs(issue)
        issues_in_sprint.append(IssueInSprint(issue, sprint, work_logs))
    return issues_in_sprint


def make_hh_mm(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours:2}h {minutes:2}m'
