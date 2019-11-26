"""

Script that solves linear program to assign students to groups. Group assignments subject to constraints specified by user in 'data/data_template.xlsx' file.

"""
import argparse
import datetime

from src.assign_groups import *


if __name__ == "__main__":

    # info and args
    parser = argparse.ArgumentParser(description="Solve linear program to assign students to groups subject to constraints.")
    parser.add_argument("filename", type=str, help="filename for Excel spreadsheet with student, group, and constraint data as your_filename_here.xlsx")
    parser.add_argument("num_solutions", type=int, help="desired number of optimal solutions")
    parser.add_argument("--pct_changed", type=float, help="desired percent (as a decimal) of student group assignments changed per optimal solution")
    parser.add_argument("-s", "--save", action="store_true", help="save student groups to Excel spreadsheet")
    parser.add_argument("-v", "--verbose", action="store_true", help="print solution(s) in terminal")
    args = parser.parse_args()

    filename = "data/" + args.filename

    num_unchanged = calculate_num_unchanged(args.pct_changed, filename)
    unique_solutions = []


    # collect optimal solutions
    for i in range(args.num_solutions):

        print(f"\nSOLUTION {i}\n")

        print("Solving with rigid maximum constraint...")
        status, solution_df = run_lp_problem(filename,
                                             elastic=False,
                                             unique_solutions=unique_solutions,
                                             num_unchanged=num_unchanged)

        if status != "Optimal":

            print(f"{status}...")

            print("Solving with elastic maximum constraint...")
            status, solution_df = run_lp_problem(filename,
                                                 elastic=True,
                                                 unique_solutions=unique_solutions,
                                                 num_unchanged=num_unchanged)

            if status != "Optimal":

                print("Unsolvable with rigid or elastic constraint. Solution "+status)
                break

        print(f"{status}...\n")

        # store unique optimal solution
        unique_solutions.append(solution_df)

        # display student groups
        if args.verbose:

            for name, group in solution_df.groupby("group"):

                print(f"GROUP {name}:\n")
                for n in group["name"].values:
                    print(f"\t{n}")
                print()

    # save student groups
    if args.save:

        # output filename as "groupings_yyyymmdd_hhmmss.xlsx"
        output_filename = "results/groupings_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+".xlsx"

        with pd.ExcelWriter(output_filename) as writer:
            for idx, solution_df in enumerate(unique_solutions):
                solution_df.sort_values("group").to_excel(writer, sheet_name=f"Solution_{idx}", index=False)

        print(f"Solution(s) saved as \"{output_filename}\"")

