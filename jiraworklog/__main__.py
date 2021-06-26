import argparse
import time

from jiraworklog.jira import make_jira
from jiraworklog.util import make_time_spent_issues, show_total_time_spent, \
    show_all_time_spent_issues, show_most_time_spent_issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('server_url', help='Server URL')
    parser.add_argument('jql', help='Jira Query Language')
    parser.add_argument('-b', dest='board_id', help='Board ID')
    parser.add_argument('-s', dest='sprint_id', help='Sprint ID')
    parser.add_argument('--duration', dest='num_most_time_spend_issues',
                        type=int,
                        help='Show N most time spent issues (N=0 for all)')

    args = parser.parse_args()

    jira = make_jira(args.server_url)
    start_time = time.time()
    print(f'Start search issues... "{args.jql}"')
    issues = jira.search_issues(args.jql)
    search_time = time.time() - start_time
    print(f'Search issues done. Find: {len(issues)} issues, '
          f'Spent time: {search_time} seconds')
    time_spent_issues = make_time_spent_issues(args.board_id, issues, jira,
                                               args.sprint_id)
    show_total_time_spent(time_spent_issues)
    if args.num_most_time_spend_issues is not None:
        show_all_issues = args.num_most_time_spend_issues == 0
        if show_all_issues:
            show_all_time_spent_issues(time_spent_issues)
        else:
            show_most_time_spent_issues(time_spent_issues,
                                        args.num_most_time_spend_issues)


if __name__ == '__main__':
    main()
