class Issue:
    def __init__(self, raw_issue):
        self._raw_issue = raw_issue

    @property
    def time_spent_in_second(self):
        return self._raw_issue.fields.timespent
