from unittest.mock import MagicMock

from jiraworklog.sprint_worklog import SprintWorkLogs

TIME_SPENT_IN_SECONDS = 3600


def test_no_issue():
    jira = MagicMock()
    sprint = MagicMock()
    assert 0 == SprintWorkLogs(jira, sprint, []).compute()


def test_no_work_log_in_sprint():
    jira, sprint = mock_jira_and_sprint(['work_log_out_of_sprint'])
    issue = MagicMock()
    assert 0 == SprintWorkLogs(jira, sprint, [issue]).compute()


def test_one_work_log_in_sprint():
    jira, sprint = mock_jira_and_sprint(['work_log_in_sprint'])
    issue = MagicMock()
    sprint_work_logs = SprintWorkLogs(jira, sprint, [issue])
    assert TIME_SPENT_IN_SECONDS == sprint_work_logs.compute()


def test_multiple_work_log_in_sprint():
    jira, sprint = mock_jira_and_sprint(
        ['work_log_out_of_sprint', 'work_log_in_sprint'])
    issue = MagicMock()
    sprint_work_logs = SprintWorkLogs(jira, sprint, [issue])
    assert TIME_SPENT_IN_SECONDS == sprint_work_logs.compute()


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
        if work_log_flag == 'work_log_out_of_sprint':
            logged_time = sprint.start_time - 10
        else:
            logged_time = (sprint.start_time + sprint.end_time) / 2
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
