from typing import Optional

EPIC_LINK_FIELD_NAME = 'customfield_11402'
EPIC_NAME_FIELD_NAME = 'customfield_11404'


class IssueType:
    TASK = 'Task'
    BUG = 'BUG'
    SUB_TASK = 'Sub-task'
    EPIC = 'Epic'


class Issue:
    def __init__(self, raw_issue):
        self._raw_issue = raw_issue

    @property
    def key(self) -> str:
        return self._raw_issue.key

    @property
    def assignee(self) -> Optional[str]:
        if self._raw_issue.fields.assignee is None:
            return None
        return self._raw_issue.fields.assignee.name

    @property
    def summary(self) -> str:
        return self._raw_issue.fields.summary

    @property
    def time_spent_in_second(self) -> int:
        if self._raw_issue.fields.timespent:
            return self._raw_issue.fields.timespent
        return 0

    @property
    def epic_link(self) -> str:
        epic_link = getattr(self._raw_issue.fields, EPIC_LINK_FIELD_NAME)
        return epic_link

    @property
    def epic_name(self) -> str:
        epic_name = getattr(self._raw_issue.fields, EPIC_NAME_FIELD_NAME)
        return epic_name

    @property
    def parent_issue_key(self) -> Optional[str]:
        parent_issue = getattr(self._raw_issue.fields, 'parent', None)
        if not parent_issue:
            return None
        return parent_issue.key

    @property
    def type(self) -> str:
        return self._raw_issue.fields.issuetype.name
