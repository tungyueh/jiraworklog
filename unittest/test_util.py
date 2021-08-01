import unittest
from unittest.mock import MagicMock

from jiraworklog.issue import IssueType

SECONDS_IN_MINUTE = 60

from jiraworklog.util import make_hh_mm, SECONDS_IN_HOUR, get_sprint, \
    make_issue_work_logs_map, make_issue_work_logs_in_sprint_map, \
    get_total_time_spent, make_total_time_spent_message, \
    get_assignee_time_spent_map, get_issue_time_spent_map, \
    sort_issue_by_time_spent, make_issue_summary, get_issue_epic_link_map, \
    get_epic_link_time_spent_map


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


def mock_jira(active_sprint=None, get_sprint=None, work_logs=None,
              get_issue=None):
    jira = MagicMock()
    jira.active_sprint.return_value = active_sprint
    jira.get_sprint.return_value = get_sprint
    jira.work_logs.return_value = work_logs
    jira.get_issue.return_value = get_issue
    return jira


def mock_issue(epic_link=None, type=None):
    issue = MagicMock()
    issue.epic_link = epic_link
    issue.type = type
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


def mock_work_log(logged_time=None, time_spent_in_seconds=None,
                  author_name=None):
    work_log = MagicMock()
    work_log.logged_time = logged_time
    work_log.time_spent_in_seconds = time_spent_in_seconds
    work_log.author_name = author_name
    return work_log


def mock_sprint(start_time=None, end_time=None):
    sprint = MagicMock()
    sprint.start_time = start_time
    sprint.end_time = end_time
    return sprint


class TestGetTotalTimeSpent(unittest.TestCase):
    def test_no_issue(self):
        total_seconds = get_total_time_spent({})
        self.assertEqual(0, total_seconds)

    def test_issue_with_no_work_log(self):
        issue = mock_issue()
        total_seconds = get_total_time_spent({issue: []})
        self.assertEqual(0, total_seconds)

    def test_issue_with_work_log(self):
        issue = mock_issue()
        time_spent_in_seconds = 1
        work_log = mock_work_log(time_spent_in_seconds=time_spent_in_seconds)
        total_seconds = get_total_time_spent({issue: [work_log]})
        self.assertEqual(time_spent_in_seconds, total_seconds)


class TestGetAssigneeTimeSpentMap(unittest.TestCase):
    def setUp(self) -> None:
        self.author_one_name = 'foo'
        self.author_two_name = 'bar'
        self.time_spent = 1

    def test_one_author_with_one_work_log(self):
        expect_assignee_map = {self.author_one_name: self.time_spent}
        work_log = mock_work_log(author_name=self.author_one_name,
                                 time_spent_in_seconds=self.time_spent)
        issue_map = {MagicMock(): [work_log]}
        actual_assignee_map = get_assignee_time_spent_map(issue_map)
        self.assertDictEqual(expect_assignee_map, actual_assignee_map)

    def test_one_author_with_two_work_log(self):
        expect_assignee_map = {self.author_one_name: self.time_spent * 2}
        work_log_one = mock_work_log(author_name=self.author_one_name,
                                     time_spent_in_seconds=self.time_spent)
        work_log_two = mock_work_log(author_name=self.author_one_name,
                                     time_spent_in_seconds=self.time_spent)
        issue_map = {MagicMock(): [work_log_one, work_log_two]}
        actual_assignee_map = get_assignee_time_spent_map(issue_map)
        self.assertDictEqual(expect_assignee_map, actual_assignee_map)

    def test_two_author(self):
        expect_assignee_map = {self.author_one_name: self.time_spent,
                               self.author_two_name: self.time_spent}
        work_log_one = mock_work_log(author_name=self.author_one_name,
                                     time_spent_in_seconds=self.time_spent)
        work_log_two = mock_work_log(author_name=self.author_two_name,
                                     time_spent_in_seconds=self.time_spent)
        issue_map = {MagicMock(): [work_log_one, work_log_two]}
        actual_assignee_map = get_assignee_time_spent_map(issue_map)
        self.assertDictEqual(expect_assignee_map, actual_assignee_map)


class TestMakeTotalTimeSpentMessage(unittest.TestCase):
    def test_0m(self):
        message = make_total_time_spent_message(0)
        self.assertEqual('Total time spent: 0.00 hours', message)

    def test_10m(self):
        message = make_total_time_spent_message(10 * SECONDS_IN_MINUTE)
        self.assertEqual('Total time spent: 0.17 hours', message)

    def test_15m(self):
        message = make_total_time_spent_message(15 * SECONDS_IN_MINUTE)
        self.assertEqual('Total time spent: 0.25 hours', message)

    def test_30m(self):
        message = make_total_time_spent_message(30 * SECONDS_IN_MINUTE)
        self.assertEqual('Total time spent: 0.50 hours', message)

    def test_1h(self):
        message = make_total_time_spent_message(1 * SECONDS_IN_HOUR)
        self.assertEqual('Total time spent: 1.00 hours', message)


class TestGetIssueTimeSpentMap(unittest.TestCase):
    def test_no_issue(self):
        issue_work_log_map = {}
        issue_time_spent_map = get_issue_time_spent_map(issue_work_log_map)
        self.assertFalse(issue_time_spent_map)

    def test_issue_with_no_work_log(self):
        issue = mock_issue()
        issue_work_log_map = {issue: []}
        issue_time_spent_map = get_issue_time_spent_map(issue_work_log_map)
        self.assertDictEqual({issue: 0}, issue_time_spent_map)

    def test_issue_with_work_log(self):
        issue = mock_issue()
        work_log = mock_work_log(time_spent_in_seconds=1)
        issue_work_log_map = {issue: [work_log]}
        issue_time_spent_map = get_issue_time_spent_map(issue_work_log_map)
        self.assertDictEqual({issue: 1}, issue_time_spent_map)


class TestSortIssueByTimeSpent(unittest.TestCase):
    def test_no_issue(self):
        issue_map = {}
        sorted_issue_map = sort_issue_by_time_spent(issue_map)
        self.assertFalse(sorted_issue_map)

    def test_two_issue(self):
        issue_one = mock_issue()
        issue_two = mock_issue()
        issue_map = {issue_one: 1, issue_two: 2}
        sorted_issue_map = sort_issue_by_time_spent(issue_map)
        excpect_issue_map = {issue_two: 2, issue_one: 1}
        self.assertDictEqual(excpect_issue_map, sorted_issue_map)


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
    return num_hour * SECONDS_IN_HOUR + num_minute * SECONDS_IN_MINUTE


class TestGetIssueEpicLinkMap(unittest.TestCase):
    def test_issue_with_epic_link(self):
        epic_link = 'foobar'
        issue = mock_issue(epic_link=epic_link)
        issue_epic_map = get_issue_epic_link_map([issue], None)
        self.assertEqual(epic_link, issue_epic_map[issue])

    def test_sub_task_issue_parent_with_epic_link(self):
        issue = mock_issue(type=IssueType.SUB_TASK)
        epic_link = 'foobar'
        parent_issue = mock_issue(epic_link=epic_link)
        jira = mock_jira(get_issue=parent_issue)
        issue_epic_map = get_issue_epic_link_map([issue], jira)
        self.assertEqual(epic_link, issue_epic_map[issue])


class TestGetEpicLinkTimeSpentMap(unittest.TestCase):
    def test_issue_without_epic_link(self):
        issue = mock_issue()
        issue_work_log_map = {issue: []}
        issue_epic_map = {issue: None}
        epic_link_map = get_epic_link_time_spent_map(issue_work_log_map,
                                                     issue_epic_map)
        self.assertDictEqual({None: 0}, epic_link_map)

    def test_issue_with_epic_link(self):
        issue = mock_issue()
        issue_work_log_map = {issue: []}
        epic_link = 'foobar'
        issue_epic_map = {issue: epic_link}
        epic_link_map = get_epic_link_time_spent_map(issue_work_log_map,
                                                     issue_epic_map)
        self.assertDictEqual({epic_link: 0}, epic_link_map)

