from abc import ABC, abstractmethod
from typing import List

from jiraworklog.sprint import Sprint
from jiraworklog.worklog import WorkLog


class IssueInterface(ABC):
    @property
    @abstractmethod
    def time_spent_in_second(self):
        raise NotImplementedError


class Issue(IssueInterface):
    def __init__(self, raw_issue):
        self._raw_issue = raw_issue

    @property
    def key(self):
        return self._raw_issue.key

    @property
    def time_spent_in_second(self):
        if self._raw_issue.fields.timespent:
            return self._raw_issue.fields.timespent
        return 0

    @property
    def assignee(self):
        return self._raw_issue.fields.assignee.name


class IssueInSprint(IssueInterface):
    def __init__(self, sprint: Sprint, work_logs: List[WorkLog]):
        self._sprint = sprint
        self._work_logs = work_logs

    @property
    def time_spent_in_second(self) -> int:
        total_seconds = 0
        for work_log in self._work_logs:
            if self._is_work_log_in_sprint(work_log):
                total_seconds += work_log.time_spent_in_seconds
        return total_seconds

    def _is_work_log_in_sprint(self, work_log):
        sprint_start = self._sprint.start_time
        sprint_end = self._sprint.end_time + 86400
        return sprint_start <= work_log.logged_time <= sprint_end
