import unittest
from unittest.mock import MagicMock

from jiraworklog.issue import Issue

from jiraworklog.util import make_hh_mm, SECONDS_IN_HOUR, get_sprint, \
    make_issue_work_logs_map


class TestGetSprint(unittest.TestCase):
    def test_board_id(self):
        mock_jira = MagicMock()
        expect_sprint = self.make_sprint()
        mock_jira.active_sprint.return_value = expect_sprint
        actual_sprint = get_sprint(jira=mock_jira, board_id=1, sprint_id=None)
        self.assertEqual(actual_sprint, expect_sprint)

    def test_sprint_id(self):
        mock_jira = MagicMock()
        expect_sprint = self.make_sprint()
        mock_jira.get_sprint.return_value = expect_sprint
        actual_sprint = get_sprint(jira=mock_jira, board_id=None, sprint_id=1)
        self.assertEqual(actual_sprint, expect_sprint)

    def test_no_board_id_and_sprint_id(self):
        sprint = get_sprint(jira=MagicMock(), board_id=None, sprint_id=None)
        self.assertIsNone(sprint)

    def make_sprint(self):
        s = MagicMock()
        s.state = 'ACTIVE'
        s.id = 0
        return s


class TestMakeIssueWorkLogsMap(unittest.TestCase):
    def test_no_issue(self):
        issues_map = make_issue_work_logs_map(jira=MagicMock(), issues=[])
        self.assertFalse(issues_map)

    def test_issue_with_no_work_log(self):
        mock_jira = self.mock_jira(work_logs=[])
        mock_issue = Issue(mock_raw_issue())
        issues_map = make_issue_work_logs_map(jira=mock_jira,
                                              issues=[mock_issue])
        self.assertDictEqual({mock_issue: []}, issues_map)

    def test_issue_with_work_log(self):
        mock_work_log = MagicMock()
        mock_jira = self.mock_jira(work_logs=[mock_work_log])
        mock_issue = Issue(mock_raw_issue())
        issues_map = make_issue_work_logs_map(jira=mock_jira,
                                              issues=[mock_issue])
        self.assertDictEqual({mock_issue: [mock_work_log]}, issues_map)

    def mock_jira(self, work_logs):
        mock_jira = MagicMock()
        mock_jira.work_logs.return_value = work_logs
        return mock_jira


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
