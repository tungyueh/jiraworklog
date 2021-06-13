from jiraworklog.sprint import Sprint, TIMESTAMP


def test_start_time():
    start_date = '31/May/21 3:12 PM'
    start_time = Sprint({'startDate': start_date}).start_time
    assert isinstance(start_time, TIMESTAMP)


def test_end_time():
    end_date = '11/Jun/21 7:12 AM'
    end_time = Sprint({'endDate': end_date}).end_time
    assert isinstance(end_time, TIMESTAMP)
