from jiraworklog.issues_worklog import IssuesWorkLog


class MockIssue:
    def __init__(self, timespent):
        self._timespent = timespent

    @property
    def time_spent_in_second(self):
        return self._timespent


def test_no_issue():
    assert 0 == IssuesWorkLog([]).compute()


def test_one_issue():
    timespent = 3600
    issue = MockIssue(timespent)
    assert timespent == IssuesWorkLog([issue]).compute()


def test_multiple_issue():
    timespent = 3600
    issues_count = 10
    issues = [MockIssue(timespent) for _ in range(issues_count)]
    assert timespent*issues_count == IssuesWorkLog(issues).compute()
