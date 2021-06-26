# JIRA Work Log
[![Build Status](https://api.travis-ci.com/tungyueh/jiraworklog.svg?branch=master)](https://travis-ci.com/tungyueh/jiraworklog)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

Calculate work log from JIRA issue
## Usage
###  Find total time spent in hours
python -m jiraworklog \<JIRA Server URL\> \<JQL\>
###  Find total time spent in hours in active sprint
python -m jiraworklog \<JIRA Server URL\> \<JQL\> -b \<Board ID\>
###  Find total time spent in hours in certain sprint
python -m jiraworklog \<JIRA Server URL\> \<JQL\> -s \<Sprint ID\>
### Show N most time spent issues
python -m jiraworklog \<JIRA Server URL\> \<JQL\> --duration \<NUM\>
## netrc file format
machine \<hostname\> login \<username\> password \<password\>
