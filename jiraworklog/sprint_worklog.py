from typing import List

from jiraworklog.issue import Issue
from jiraworklog.jira import Jira
from jiraworklog.sprint import Sprint


class SprintWorkLogs:
    def __init__(self, jira: Jira, sprint: Sprint, issues: List[Issue]):
        self._jira = jira
        self._sprint = sprint
        self._issues = issues

    def compute(self) -> int:
        total_seconds = 0
        for issue in self._issues:
            total_seconds += self._time_spent_in_sprint(issue)
        return total_seconds

    def _time_spent_in_sprint(self, issue):
        total_seconds = 0
        for work_log in self._jira.work_logs(issue):
            if self._is_work_log_in_sprint(work_log):
                total_seconds += work_log.time_spent_in_seconds
        return total_seconds

    def _is_work_log_in_sprint(self, work_log):
        sprint_start = self._sprint.start_time
        sprint_end = self._sprint.end_time + 86400
        return sprint_start <= work_log.logged_time <= sprint_end
