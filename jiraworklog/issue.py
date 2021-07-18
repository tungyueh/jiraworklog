from typing import Optional


class Issue:
    def __init__(self, raw_issue):
        self._raw_issue = raw_issue

    @property
    def key(self):
        return self._raw_issue.key

    @property
    def assignee(self) -> Optional[str]:
        if self._raw_issue.fields.assignee is None:
            return None
        return self._raw_issue.fields.assignee.name

    @property
    def summary(self):
        return self._raw_issue.fields.summary

    @property
    def time_spent_in_second(self):
        if self._raw_issue.fields.timespent:
            return self._raw_issue.fields.timespent
        return 0
