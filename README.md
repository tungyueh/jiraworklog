# JIRA Work Log
[![Build Status](https://api.travis-ci.com/tungyueh/jiraworklog.svg?branch=master)](https://travis-ci.com/tungyueh/jiraworklog)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

* Purpose: Calculate work log from JIRA issue in certain sprint
* Motivation: The issue may move from sprint to sprint so we are hard to know how much time we spent on this issue.
* Ability:
  * Get total time logged during sprint
  * Get people total time logged during sprint
  * Get most time spent issues during sprint
## Usage
###  Find total time spent in hours
python -m jiraworklog \<JIRA Server URL\> \<JQL\>
###  Find total time spent in hours in active sprint
python -m jiraworklog \<JIRA Server URL\> \<JQL\> -b \<Board ID\>
###  Find total time spent in hours in certain sprint
python -m jiraworklog \<JIRA Server URL\> \<JQL\> -s \<Sprint ID\>
### Show N most time spent issues
python -m jiraworklog \<JIRA Server URL\> \<JQL\> --duration \<NUM\>
### Show total time spent by assignee
python -m jiraworklog \<JIRA Server URL\> \<JQL\> --assignee
### Show Help
python -m jiraworklog -h
## netrc file format
machine \<hostname\> login \<username\> password \<password\>
