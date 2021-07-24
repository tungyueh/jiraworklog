from collections import defaultdict
from typing import List, Dict

from jiraworklog.issue import Issue
from jiraworklog.worklog import WorkLog

IssueTimeSpentMap = Dict[Issue, int]
AssigneeTimeSpentMap = Dict[str, int]
IssueWorkLogMap = Dict[Issue, List[WorkLog]]

SECONDS_IN_HOUR = 3600


def get_sprint(jira, board_id, sprint_id):
    sprint = None
    if board_id:
        sprint = jira.active_sprint(board_id)
    elif sprint_id:
        sprint = jira.get_sprint(sprint_id)
    return sprint


def make_issue_work_logs_map(jira, issues) -> IssueWorkLogMap:
    issue_work_logs_map = {}
    for issue in issues:
        work_logs = jira.work_logs(issue)
        issue_work_logs_map[issue] = work_logs
        if len(issue_work_logs_map) % 50 == 0:
            print(f'Collect Work Log on {len(issue_work_logs_map)} issues...')
    return issue_work_logs_map


def make_issue_work_logs_in_sprint_map(jira, issues, sprint) -> \
        IssueWorkLogMap:
    issue_work_logs_in_sprint_map = {}
    issue_work_logs_map = make_issue_work_logs_map(jira, issues)
    for issue, work_logs in issue_work_logs_map.items():
        work_logs_in_sprint = get_work_logs_in_sprint(sprint, work_logs)
        issue_work_logs_in_sprint_map[issue] = work_logs_in_sprint
    return issue_work_logs_in_sprint_map


def get_work_logs_in_sprint(sprint, work_logs) -> List[WorkLog]:
    work_logs_in_sprint = []
    for work_log in work_logs:
        if is_work_log_in_sprint(sprint, work_log):
            work_logs_in_sprint.append(work_log)
    return work_logs_in_sprint


def is_work_log_in_sprint(sprint, work_log) -> bool:
    sprint_start = sprint.start_time
    sprint_end = sprint.end_time + 86400
    return sprint_start <= work_log.logged_time <= sprint_end


def show_total_time_spent(issue_map: IssueWorkLogMap):
    total_seconds = 0
    for work_logs in issue_map.values():
        total_seconds += get_total_time_spent_in_seconds(work_logs)
    print(make_total_time_spent_message(total_seconds))


def get_total_time_spent_in_seconds(work_logs: List[WorkLog]) -> int:
    total_seconds = 0
    for work_log in work_logs:
        total_seconds += work_log.time_spent_in_seconds
    return total_seconds


def make_total_time_spent_message(total_seconds: int) -> str:
    return f'Total time spent: {total_seconds / SECONDS_IN_HOUR:.2f} hours'


def show_total_time_spent_by_assignee(issue_map: IssueWorkLogMap):
    assignee_time_spent_map = get_assignee_time_spent_map(issue_map)
    for author_name, total_seconds in assignee_time_spent_map.items():
        total_time_spent_msg = make_total_time_spent_message(total_seconds)
        print(f'{author_name:12} {total_time_spent_msg}')


def get_assignee_time_spent_map(issue_map) -> AssigneeTimeSpentMap:
    assignee_time_spent_map: AssigneeTimeSpentMap = defaultdict(int)
    for work_logs in issue_map.values():
        for work_log in work_logs:
            assignee_time_spent_map[
                work_log.author_name] += work_log.time_spent_in_seconds
    return assignee_time_spent_map


def get_issue_time_spent_map(issue_map: IssueWorkLogMap) -> \
        IssueTimeSpentMap:
    issue_time_spent_map: IssueTimeSpentMap = {}
    for issue, work_logs in issue_map.items():
        total_seconds = get_total_time_spent_in_seconds(work_logs)
        issue_time_spent_map[issue] = total_seconds
    return issue_time_spent_map


def sort_issue_by_time_spent(issue_time_spent_map: IssueTimeSpentMap) -> \
        IssueTimeSpentMap:
    issues = {}
    for issue, time_spent in sorted(issue_time_spent_map.items(),
                                    key=lambda item: item[1], reverse=True):
        issues[issue] = time_spent
    return issues


def make_issue_summary(issue, time_spent_in_second):
    return f'{issue.key} {issue.assignee:12} ' \
           f'{make_hh_mm(time_spent_in_second)} ' \
           f'{issue.summary}'


def show_most_time_spent_issues(issue_map: IssueWorkLogMap,
                                num_most_time_spend_issues: int):
    issue_time_spent_map = get_issue_time_spent_map(issue_map)
    issue_time_spent_map = sort_issue_by_time_spent(issue_time_spent_map)
    count = 0
    for issue, time_spent_in_second in issue_time_spent_map.items():
        if count == num_most_time_spend_issues:
            return
        count += 1
        if time_spent_in_second:
            print(make_issue_summary(issue, time_spent_in_second))


def make_hh_mm(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours:2}h {minutes:2}m'
