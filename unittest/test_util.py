import unittest

from jiraworklog.util import make_hh_mm, SECONDS_IN_HOUR


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
