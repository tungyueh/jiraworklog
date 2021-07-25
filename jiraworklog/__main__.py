import argparse
import time

from jiraworklog.jira import make_jira
from jiraworklog.util import (make_issue_work_logs_map, get_total_time_spent,
                              get_sprint, make_issue_work_logs_in_sprint_map,
                              make_total_time_spent_message,
                              get_assignee_time_spent_map,
                              get_issue_time_spent_map,
                              sort_issue_by_time_spent, make_issue_summary)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('server_url', help='Server URL')
    parser.add_argument('jql', help='Jira Query Language')
    parser.add_argument('-b', dest='board_id', help='Board ID')
    parser.add_argument('-s', dest='sprint_id', help='Sprint ID')
    parser.add_argument('--duration', dest='num_issues', type=int,
                        help='Show N most time spent issues (N=0 for all)')
    parser.add_argument('--assignee', action='store_true')

    args = parser.parse_args()

    jira = make_jira(args.server_url)
    start_time = time.time()
    print(f'Start search issues... "{args.jql}"')
    issues = jira.search_issues(args.jql)
    search_time = time.time() - start_time
    print(f'Search issues done. Find: {len(issues)} issues, '
          f'Spent time: {search_time:.2f} seconds')

    sprint = get_sprint(jira, args.board_id, args.sprint_id)
    work_log_only_in_sprint = args.board_id or args.sprint_id
    if work_log_only_in_sprint and not sprint:
        print('No Sprint')
        return

    if work_log_only_in_sprint:
        issue_work_logs_map = make_issue_work_logs_in_sprint_map(jira, issues,
                                                                 sprint)
    else:
        issue_work_logs_map = make_issue_work_logs_map(jira, issues)
    total_seconds = get_total_time_spent(issue_work_logs_map)
    print(make_total_time_spent_message(total_seconds))
    if args.assignee:
        show_time_spent_by_assignee(issue_work_logs_map)
    if args.num_issues is not None:
        num_issues = args.num_issues if args.num_issues else len(issues)
        show_most_time_spent_issues(issue_work_logs_map, num_issues)


def show_time_spent_by_assignee(issue_map):
    print('=== time spent by assignee ===')
    assignee_map = get_assignee_time_spent_map(issue_map)
    for author_name, total_seconds in assignee_map.items():
        total_time_spent_msg = make_total_time_spent_message(total_seconds)
        print(f'{author_name:12} {total_time_spent_msg}')


def show_most_time_spent_issues(issue_map, num_issues):
    print('=== most time spent issues ===')
    time_spent_map = get_issue_time_spent_map(issue_map)
    time_spent_map = sort_issue_by_time_spent(time_spent_map)
    for issue, time_spent in list(time_spent_map.items())[:num_issues]:
        if time_spent:
            print(make_issue_summary(issue, time_spent))


if __name__ == '__main__':
    main()
