from unittest.mock import MagicMock

from jiraworklog.issue import Issue
from jiraworklog.util import make_issues_in_sprint


def test_issue_no_timespent():
    issue = Issue(mock_raw_issue(time_spent=None))
    assert 0 == issue.time_spent_in_second


def test_issue_timespent():
    time_spent = 3600
    issue = Issue(mock_raw_issue(time_spent))
    assert time_spent == issue.time_spent_in_second


def test_work_log_in_past_sprint():
    jira, sprint = mock_jira_and_sprint(['past'])
    issue = MagicMock()
    issues = make_issues_in_sprint(jira, sprint, [issue])
    assert 0 == sum_time_spent_in_issues(issues)


def test_work_log_in_current_sprint():
    jira, sprint = mock_jira_and_sprint(['now'])
    issue = MagicMock()
    issues = make_issues_in_sprint(jira, sprint, [issue])
    assert TIME_SPENT_IN_SECONDS == sum_time_spent_in_issues(issues)


def test_work_log_in_future_sprint():
    jira, sprint = mock_jira_and_sprint(['future'])
    issue = MagicMock()
    issues = make_issues_in_sprint(jira, sprint, [issue])
    assert 0 == sum_time_spent_in_issues(issues)


def test_unassigned_issue():
    issue = Issue(mock_raw_issue(assignee_name=None))
    assert None is issue.assignee


def test_assigned_issue():
    assignee_name = 'AssigneeName'
    issue = Issue(mock_raw_issue(assignee_name=assignee_name))
    assert assignee_name == issue.assignee


def mock_raw_issue(time_spent=None, assignee_name=None):
    m = MagicMock()
    m.fields.timespent = time_spent
    if assignee_name:
        m.fields.assignee = mock_assignee(assignee_name)
    else:
        m.fields.assignee = None
    return m


def mock_assignee(assignee_name):
    assignee = MagicMock()
    assignee.name = assignee_name
    return assignee


def sum_time_spent_in_issues(issues):
    return sum([issue.time_spent_in_second for issue in issues])


TIME_SPENT_IN_SECONDS = 3600


def mock_jira_and_sprint(work_log_flags):
    sprint = mock_sprint()
    work_logs = mock_work_logs(sprint, work_log_flags)
    jira = mock_jira(work_logs)
    return jira, sprint


def mock_sprint():
    sprint = MagicMock()
    sprint.start_time = 10
    sprint.end_time = 20
    return sprint


def mock_work_logs(sprint, work_log_flags):
    work_logs = []
    for work_log_flag in work_log_flags:
        if work_log_flag == 'past':
            logged_time = sprint.start_time - 10
        elif work_log_flag == 'now':
            logged_time = (sprint.start_time + sprint.end_time) / 2
        elif work_log_flag == 'future':
            logged_time = sprint.end_time + 86410
        else:
            assert False, f'invalid {work_log_flag}'
        work_log = mock_work_log(logged_time)
        work_logs.append(work_log)
    return work_logs


def mock_work_log(logged_time):
    work_log = MagicMock()
    work_log.logged_time = logged_time
    work_log.time_spent_in_seconds = TIME_SPENT_IN_SECONDS
    return work_log


def mock_jira(work_logs):
    jira = MagicMock()
    jira.work_logs.return_value = work_logs
    return jira