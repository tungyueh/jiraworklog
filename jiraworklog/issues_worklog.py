from typing import List

from jiraworklog.issue import Issue


class IssuesWorkLog:
    def __init__(self, issues: List[Issue]):
        self._issues = issues

    def compute(self) -> int:
        total_seconds = 0
        for issue in self._issues:
            if issue.time_spent_in_second:
                total_seconds += issue.time_spent_in_second
        return total_seconds
