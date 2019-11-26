"""

Script to check student groups for constraint satisfaction.

Example:

    SOLUTION 0

    WITH...
        index 0: ok

    NOT WITH...
        index 0: ok
        index 1: ok
        ...

    ...

"""
import argparse

from src.assign_groups import *
from src.test_groups import *


def import_optimal_groupings(filename):
    """
    Import list of unique solutions (groupings) from Excel spreadsheet.
    """
    groupings = pd.read_excel(filename, sheet_name=None)
    sheet_names = list(groupings.keys())

    unique_solutions = []
    for sheet_name in sheet_names:
        unique_solutions.append(groupings[sheet_name])

    return(unique_solutions)


if __name__ == "__main__":

    # info and args
    parser = argparse.ArgumentParser(description='Test student groups for constraint satisfaction.')
    parser.add_argument('data_filename', type=str, help='filename for Excel spreadsheet with student, group, and constraint data as your_filename_here.xlsx')
    parser.add_argument('groups_filename', type=str, help='filename for Excel spreadsheet with student groups as your_filename_here.xlsx')
    args = parser.parse_args()

    data_filename = 'data/' + args.data_filename
    groups_filename = 'results/' + args.groups_filename

    unique_solutions = import_optimal_groupings(groups_filename)

    person_df = import_from_template(data_filename, "Person Setup")
    with_df = import_from_template(data_filename, "Constraint - With")
    not_with_df = import_from_template(data_filename, "Constraint - Not With")
    in_df = import_from_template(data_filename, "Constraint - In")
    not_in_df = import_from_template(data_filename, "Constraint - Not In")
    hom_df = import_from_template(data_filename,"Constraint - Homogenous")
    max_df = import_from_template(data_filename, "Constraint - Maximum")


    for idx, solution_df in enumerate(unique_solutions):

        print(f"\nSOLUTION {idx}\n")
        df = pd.merge(person_df, solution_df, on="name")

        print("WITH...")
        test_with_constraint(with_df, df, False)

        print("\nNOT WITH...")
        test_not_with_constraint(not_with_df, df, False)

        print("\nIN...")
        test_in_constraint(in_df, df, False)

        print("\nNOT IN...")
        test_not_in_constraint(not_in_df, df, False)

        print("\nHOMOGENOUS...")
        test_homogenous_constraint(hom_df, df, False)

        print("\nMAXIMUM...")
        test_maximum_constraint(max_df, df, False)

        print()


