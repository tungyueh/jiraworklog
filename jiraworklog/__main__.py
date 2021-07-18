import argparse
import time

from jiraworklog.jira import make_jira
from jiraworklog.util import make_issue_work_logs_map, show_total_time_spent, \
    show_all_time_spent_issues, show_most_time_spent_issues, \
    show_total_time_spent_by_assignee, get_sprint, \
    make_issue_work_logs_in_sprint_map


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('server_url', help='Server URL')
    parser.add_argument('jql', help='Jira Query Language')
    parser.add_argument('-b', dest='board_id', help='Board ID')
    parser.add_argument('-s', dest='sprint_id', help='Sprint ID')
    parser.add_argument('--duration', dest='num_most_time_spend_issues',
                        type=int,
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

    if args.board_id or args.sprint_id:
        sprint = get_sprint(jira, args.board_id, args.sprint_id)
        if not sprint:
            print('No Sprint')
            return
        issue_work_logs_map = make_issue_work_logs_in_sprint_map(jira, issues,
                                                                 sprint)
    else:
        issue_work_logs_map = make_issue_work_logs_map(jira, issues)
    show_total_time_spent(issue_work_logs_map)
    if args.assignee:
        print('=== time spent by assignee ===')
        show_total_time_spent_by_assignee(issue_work_logs_map)
    if args.num_most_time_spend_issues is not None:
        print('=== most time spent issues ===')
        show_all_issues = args.num_most_time_spend_issues == 0
        if show_all_issues:
            show_all_time_spent_issues(issue_work_logs_map)
        else:
            show_most_time_spent_issues(issue_work_logs_map,
                                        args.num_most_time_spend_issues)


if __name__ == '__main__':
    main()
