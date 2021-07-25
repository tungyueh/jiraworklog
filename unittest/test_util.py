import unittest
from unittest.mock import MagicMock


from jiraworklog.util import make_hh_mm, SECONDS_IN_HOUR, get_sprint, \
    make_issue_work_logs_map, make_issue_work_logs_in_sprint_map, \
    get_total_time_spent


class TestGetSprint(unittest.TestCase):
    def test_board_id(self):
        expect_sprint = mock_sprint()
        jira = mock_jira(active_sprint=expect_sprint)
        actual_sprint = get_sprint(jira=jira, board_id=1, sprint_id=None)
        self.assertEqual(actual_sprint, expect_sprint)

    def test_sprint_id(self):
        expect_sprint = mock_sprint()
        jira = mock_jira(get_sprint=expect_sprint)
        actual_sprint = get_sprint(jira=jira, board_id=None, sprint_id=1)
        self.assertEqual(actual_sprint, expect_sprint)

    def test_no_board_id_and_sprint_id(self):
        sprint = get_sprint(jira=MagicMock(), board_id=None, sprint_id=None)
        self.assertIsNone(sprint)


class TestMakeIssueWorkLogsMap(unittest.TestCase):
    def test_no_issue(self):
        issues_map = make_issue_work_logs_map(jira=MagicMock(), issues=[])
        self.assertFalse(issues_map)

    def test_issue_with_no_work_log(self):
        jira = mock_jira(work_logs=[])
        issue = mock_issue()
        issues_map = make_issue_work_logs_map(jira=jira, issues=[issue])
        self.assertDictEqual({issue: []}, issues_map)

    def test_issue_with_work_log(self):
        work_log = mock_work_log()
        jira = mock_jira(work_logs=[work_log])
        issue = mock_issue()
        issues_map = make_issue_work_logs_map(jira=jira, issues=[issue])
        self.assertDictEqual({issue: [work_log]}, issues_map)


def mock_jira(active_sprint=None, get_sprint=None, work_logs=None):
    jira = MagicMock()
    jira.active_sprint.return_value = active_sprint
    jira.get_sprint.return_value = get_sprint
    jira.work_logs.return_value = work_logs
    return jira


def mock_issue():
    issue = MagicMock()
    return issue


class TestMakeIssueWorkLogsInSprintMap(unittest.TestCase):
    def test_no_issue(self):
        issues_map = make_issue_work_logs_in_sprint_map(jira=MagicMock(),
                                                        issues=[],
                                                        sprint=MagicMock())
        self.assertFalse(issues_map)

    def test_issue_with_no_work_log(self):
        jira = mock_jira(work_logs=[])
        issue = mock_issue()
        issues_map = make_issue_work_logs_in_sprint_map(jira=jira,
                                                        issues=[issue],
                                                        sprint=MagicMock())
        self.assertDictEqual({issue: []}, issues_map)

    def test_issue_with_in_sprint_work_log(self):
        work_log = mock_work_log(logged_time=1)
        sprint = mock_sprint(start_time=0, end_time=2)
        jira = mock_jira(work_logs=[work_log])
        issue = mock_issue()
        issues_map = make_issue_work_logs_in_sprint_map(jira=jira,
                                                        issues=[issue],
                                                        sprint=sprint)
        self.assertDictEqual({issue: [work_log]}, issues_map)

    def test_issue_with_out_sprint_work_log(self):
        work_log = mock_work_log(logged_time=0)
        sprint = mock_sprint(start_time=1, end_time=2)
        jira = mock_jira(work_logs=[work_log])
        issue = mock_issue()
        issues_map = make_issue_work_logs_in_sprint_map(jira=jira,
                                                        issues=[issue],
                                                        sprint=sprint)
        self.assertDictEqual({issue: []}, issues_map)


def mock_work_log(logged_time=None, time_spent_in_seconds=None):
    work_log = MagicMock()
    work_log.logged_time = logged_time
    work_log.time_spent_in_seconds = time_spent_in_seconds
    return work_log


def mock_sprint(start_time=None, end_time=None):
    sprint = MagicMock()
    sprint.start_time = start_time
    sprint.end_time = end_time
    return sprint


class TestGetTotalTimeSpent(unittest.TestCase):
    def test_no_issue(self):
        total_seconds = get_total_time_spent({})
        self.assertEqual(0 , total_seconds)

    def test_issue_with_no_work_log(self):
        issue = mock_issue()
        total_seconds = get_total_time_spent({issue: []})
        self.assertEqual(0 , total_seconds)

    def test_issue_with_work_log(self):
        issue = mock_issue()
        time_spent_in_seconds = 1
        work_log = mock_work_log(time_spent_in_seconds=time_spent_in_seconds)
        total_seconds = get_total_time_spent({issue: [work_log]})
        self.assertEqual(time_spent_in_seconds , total_seconds)


class TestMakeHHMM(unittest.TestCase):
    def test_0m(self):
        seconds = make_seconds(0, 0)
        self.assertEqual(' 0h  0m', make_hh_mm(seconds))

    def test_10m(self):
        seconds = make_seconds(0, 10)
        self.assertEqual(' 0h 10m', make_hh_mm(seconds))

    def test_15m(self):
        seconds = make_seconds(0, 15)
        self.assertEqual(' 0h 15m', make_hh_mm(seconds))

    def test_30m(self):
        seconds = make_seconds(0, 30)
        self.assertEqual(' 0h 30m', make_hh_mm(seconds))

    def test_1h(self):
        seconds = make_seconds(1, 0)
        self.assertEqual(' 1h  0m', make_hh_mm(seconds))

    def test_1h_10m(self):
        seconds = make_seconds(1, 10)
        self.assertEqual(' 1h 10m', make_hh_mm(seconds))

    def test_1h_15m(self):
        seconds = make_seconds(1, 15)
        self.assertEqual(' 1h 15m', make_hh_mm(seconds))

    def test_1h_30m(self):
        seconds = make_seconds(1, 30)
        self.assertEqual(' 1h 30m', make_hh_mm(seconds))

    def test_1h_40m(self):
        seconds = make_seconds(1, 40)
        self.assertEqual(' 1h 40m', make_hh_mm(seconds))

    def test_2h(self):
        seconds = make_seconds(2, 0)
        self.assertEqual(' 2h  0m', make_hh_mm(seconds))


def make_seconds(num_hour, num_minute) -> int:
    return num_hour * SECONDS_IN_HOUR + num_minute * 60
