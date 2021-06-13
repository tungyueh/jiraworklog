from jiraworklog.sprint import Sprint


def test_start_time():
    start_date = '31/May/21 3:12 PM'
    assert 1622401920.0 == Sprint({'startDate': start_date}).start_time

def test_end_time():
    end_date = '11/Jun/21 7:12 AM'
    assert 1623366720.0 == Sprint({'endDate': end_date}).end_time