from datetime import datetime

TIMESTAMP = float
TIME_FORMAT_CODE = '%d/%b/%y %H:%M %p'


class Sprint:
    def __init__(self, raw_sprint):
        self._raw_sprint = raw_sprint

    @property
    def id(self) -> int:  # pylint: disable=invalid-name
        return self._raw_sprint['id']

    @property
    def start_time(self) -> TIMESTAMP:
        date = self._raw_sprint['startDate']
        return datetime.strptime(date, TIME_FORMAT_CODE).timestamp()

    @property
    def end_time(self) -> TIMESTAMP:
        date = self._raw_sprint['endDate']
        return datetime.strptime(date, TIME_FORMAT_CODE).timestamp()
