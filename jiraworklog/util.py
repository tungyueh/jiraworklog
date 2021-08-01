from collections import defaultdict
from typing import List, Dict, Optional, Set

from jiraworklog.issue import Issue, IssueType
from jiraworklog.jira import Jira
from jiraworklog.sprint import Sprint
from jiraworklog.worklog import WorkLog

IssueEpicMap = Dict[Issue, str]
IssueTimeSpentMap = Dict[Issue, int]
AssigneeTimeSpentMap = Dict[str, int]
EpicLinkTimeSpentMap = Dict[str, int]
IssueWorkLogMap = Dict[Issue, List[WorkLog]]

SECONDS_IN_HOUR = 3600


def get_sprint(jira: Jira, board_id: Optional[int],
               sprint_id: Optional[int]) -> Optional[Sprint]:
    sprint = None
    if board_id:
        sprint = jira.active_sprint(board_id)
    elif sprint_id:
        sprint = jira.get_sprint(sprint_id)
    return sprint


def make_issue_work_logs_map(jira: Jira, issues: List[Issue]) -> \
        IssueWorkLogMap:
    issue_work_logs_map = {}
    for issue in issues:
        work_logs = jira.work_logs(issue)
        issue_work_logs_map[issue] = work_logs
        if len(issue_work_logs_map) % 50 == 0:
            print(f'Collect Work Log on {len(issue_work_logs_map)} issues...')
    return issue_work_logs_map


def make_issue_work_logs_in_sprint_map(jira: Jira, issues: List[Issue],
                                       sprint: Sprint) -> IssueWorkLogMap:
    issue_work_logs_in_sprint_map = {}
    issue_work_logs_map = make_issue_work_logs_map(jira, issues)
    for issue, work_logs in issue_work_logs_map.items():
        work_logs_in_sprint = get_work_logs_in_sprint(sprint, work_logs)
        issue_work_logs_in_sprint_map[issue] = work_logs_in_sprint
    return issue_work_logs_in_sprint_map


def get_work_logs_in_sprint(sprint: Sprint, work_logs: List[WorkLog]) -> \
        List[WorkLog]:
    work_logs_in_sprint = []
    for work_log in work_logs:
        if is_work_log_in_sprint(sprint, work_log):
            work_logs_in_sprint.append(work_log)
    return work_logs_in_sprint


def is_work_log_in_sprint(sprint: Sprint, work_log: WorkLog) -> bool:
    sprint_start = sprint.start_time
    sprint_end = sprint.end_time + 86400
    return sprint_start <= work_log.logged_time <= sprint_end


def get_total_time_spent(issue_map: IssueWorkLogMap) -> int:
    total_seconds = 0
    for work_logs in issue_map.values():
        total_seconds += sum_time_spent_from_work_logs(work_logs)
    return total_seconds


def sum_time_spent_from_work_logs(work_logs: List[WorkLog]) -> int:
    total_seconds = 0
    for work_log in work_logs:
        total_seconds += work_log.time_spent_in_seconds
    return total_seconds


def make_total_time_spent_message(total_seconds: int) -> str:
    return f'Total time spent: {total_seconds / SECONDS_IN_HOUR:.2f} hours'


def get_assignee_time_spent_map(issue_map: IssueWorkLogMap) -> \
        AssigneeTimeSpentMap:
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
        total_seconds = sum_time_spent_from_work_logs(work_logs)
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


def make_hh_mm(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours:2}h {minutes:2}m'


def get_issue_epic_link_map(issues: List[Issue], jira: Jira) -> IssueEpicMap:
    issue_epic_map = dict()
    for issue in issues:
        epic_link = issue.epic_link
        if issue.type == IssueType.SUB_TASK:
            parent_issue = jira.get_issue(issue.parent_issue_key)
            epic_link = parent_issue.epic_link
        issue_epic_map[issue] = epic_link
    return issue_epic_map


def get_epic_link_name_map(epic_links: Set[str], jira: Jira) -> Dict[str, str]:
    epic_link_name_map = dict()
    for epic_link in epic_links:
        if not epic_link:
            continue
        issue = jira.get_issue(epic_link)
        epic_link_name_map[epic_link] = issue.epic_name
    return epic_link_name_map


def get_epic_link_time_spent_map(issue_work_log_map: IssueWorkLogMap,
                                 issue_epic_map: IssueEpicMap) -> \
        EpicLinkTimeSpentMap:
    epic_link_time_spent_map: EpicLinkTimeSpentMap = defaultdict(int)
    for issue, work_logs in issue_work_log_map.items():
        time_spent = sum_time_spent_from_work_logs(work_logs)
        epic_link = issue_epic_map[issue]
        epic_link_time_spent_map[epic_link] += time_spent
    return epic_link_time_spent_map
