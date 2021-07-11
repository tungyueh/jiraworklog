from datetime import datetime

TIMESTAMP = float
TIME_FORMAT_CODE = '%Y-%m-%dT%H:%M:%S.%f%z'


class WorkLog:
    def __init__(self, raw_work_log):
        self._raw_work_log = raw_work_log

    @property
    def logged_time(self) -> TIMESTAMP:
        started = self._raw_work_log.started
        return datetime.strptime(started, TIME_FORMAT_CODE).timestamp()

    @property
    def time_spent_in_seconds(self) -> int:
        return self._raw_work_log.timeSpentSeconds

    @property
    def author_name(self) -> str:
        return self._raw_work_log.author.name
