import getpass
from typing import List

from jira import JIRA
from requests.utils import get_netrc_auth

from jiraworklog.issue import Issue

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


def make_jira(server_url: URL) -> Jira:
    if not get_netrc_auth(server_url):
        user = input("Jira Username:")
        password = getpass.getpass()
        return Jira(server_url, user, password)
    return Jira(server_url)
