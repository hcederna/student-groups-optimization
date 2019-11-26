"""

Script to use with multiple student grouping solutions to review the number of students who change groups from one solution to the next. Compares student group changes by solution and by group.

Example:

    CHANGES BY SOLUTION...

    SOLUTION 0 --> SOLUTION 1
        group 1: 2
        group 2: 2
        ...

    ...

    CHANGES BY GROUP...

    GROUP 1
        solution 0 --> solution 1: 2 of 4
        solution 1 --> solution 2: 3 of 4
        ...

"""

import argparse

from src.assign_groups import *
from src.test_groups import *

from check_constraints import import_optimal_groupings


if __name__ == "__main__":

    # info and args
    parser = argparse.ArgumentParser(description='Test solutions for uniqueness. Compare changes by solution (solution 0 --> 1 by group, solution 1 --> 2 by group, ...) and compare changes by group (group 1 by solution, group 2 by solution, ...)')
    parser.add_argument('data_filename', type=str, help='filename for Excel spreadsheet with student, group, and constraint data as your_filename_here.xlsx')
    parser.add_argument('groups_filename', type=str, help='filename for Excel spreadsheet with student groups as your_filename_here.xlsx')
    args = parser.parse_args()

    data_filename = 'data/' + args.data_filename
    groups_filename = 'results/' + args.groups_filename

    unique_solutions = import_optimal_groupings(groups_filename)


    # compare solution 0 --> 1 by group, solution 1 --> 2 by group, ...
    print("\n\nCHANGES BY SOLUTION...\n")
    view_changes_by_solution(data_filename, unique_solutions, False)

    # compare group 1 by solution, group 2 by solution, ...
    print("\n\nCHANGES BY GROUP...\n")
    view_changes_by_group(data_filename, unique_solutions, False)