from unittest.mock import MagicMock

from jiraworklog.issue import Issue


def mock_raw_issue(time_spent):
    m = MagicMock()
    m.fields.timespent = time_spent
    return m


def test_issue_no_timespent():
    issue = Issue(mock_raw_issue(time_spent=None))
    assert 0 == issue.time_spent_in_second


def test_issue_timespent():
    time_spent = 3600
    issue = Issue(mock_raw_issue(time_spent))
    assert time_spent == issue.time_spent_in_second
