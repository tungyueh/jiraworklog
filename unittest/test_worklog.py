from unittest.mock import MagicMock

from jiraworklog.worklog import WorkLog, TIMESTAMP


def test_logged_time():
    started = '2021-06-02T10:29:00.000+0800'
    m = MagicMock()
    m.started = started
    assert isinstance(WorkLog(m).logged_time, TIMESTAMP)