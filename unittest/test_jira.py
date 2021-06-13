from unittest.mock import MagicMock

from jiraworklog.jira import Jira


def test_no_sprint():
    m = mock_jira_with_sprints([])
    active_sprint = Jira(m).active_sprint(0)
    assert None is active_sprint


def test_no_active_sprint():
    sprint = make_sprint(state='CLOSED')
    m = mock_jira_with_sprints([sprint])
    active_sprint = Jira(m).active_sprint(0)
    assert None is active_sprint


def test_active_sprint():
    sprint = make_sprint(state='ACTIVE')
    m = mock_jira_with_sprints([sprint])
    active_sprint = Jira(m).active_sprint(0)
    assert active_sprint


def mock_jira_with_sprints(sprints):
    m = MagicMock()
    m.sprints.return_value = sprints
    m._sprint_info.return_value = {}
    return m


def make_sprint(state):
    s = MagicMock()
    s.state = state
    s.id = 0
    return s
