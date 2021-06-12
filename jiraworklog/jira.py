import getpass
from typing import List, Optional, Dict

from jira import JIRA
from requests.utils import get_netrc_auth  # type: ignore

from jiraworklog.issue import Issue
from jiraworklog.sprint import Sprint
from jiraworklog.worklog import WorkLog

URL = str


class Jira:
    def __init__(self, server_url: URL, user=None, password=None):
        if user and password:
            self._raw_jira = JIRA(server_url, basic_auth=(user, password))
        else:
            self._raw_jira = JIRA(server_url)

    def search_issues(self, jql) -> List[Issue]:
        issues = []
        for issue in self._raw_jira.search_issues(jql):
            issues.append(Issue(issue))
        return issues

    def work_logs(self, issue: Issue) -> List[WorkLog]:
        work_logs = []
        for work_log in self._raw_jira.worklogs(issue.key):
            work_logs.append(WorkLog(work_log))
        return work_logs

    def active_sprint(self, board_id: int) -> Optional[Sprint]:
        for sprint in self._raw_jira.sprints(board_id):
            if sprint.state == 'ACTIVE':
                sprint_id = sprint.id
                sprint = self._sprint_info(board_id, sprint_id)
                return Sprint(sprint)
        return None

    def _sprint_info(self, board_id: int, sprint_id: int) -> Dict:
        sprint_info = self._raw_jira.sprint_info(board_id, sprint_id)
        return sprint_info

    def get_sprint(self, sprint_id: int) -> Sprint:
        sprint = self._raw_jira.sprint(sprint_id)
        return Sprint(sprint.raw)


def make_jira(server_url: URL) -> Jira:
    if not get_netrc_auth(server_url):
        user = input("Jira Username:")
        password = getpass.getpass()
        return Jira(server_url, user, password)
    return Jira(server_url)
