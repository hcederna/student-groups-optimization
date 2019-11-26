import pandas as pd

from src.assign_groups import import_from_template


####################
# Test Constraints #
####################

def test_with_constraint(with_df, solution_df, verbose=True):
    """
    Test to ensure specified names assigned to group together.
    """
    if verbose:
        display(with_df)

    for idx, with_row in with_df.iterrows():
        names_together = list(with_row.dropna().values)
        names_together_df = solution_df.loc[solution_df["name"].isin(names_together)]
        if names_together_df["group"].nunique() == 1:
            print(f"\tindex {idx}: ok")
        else:
            print(f"\tindex {idx}: FAILED")
            display(names_together_df)


def test_not_with_constraint(not_with_df, solution_df, verbose=True):
    """
    Test to ensure specified names assigned to different groups.
    """
    if verbose:
        display(not_with_df)

    for idx, names_separate_row in not_with_df.iterrows():
        names_separate = list(names_separate_row.dropna().values)
        names_separate_df = solution_df.loc[solution_df["name"].isin(names_separate)]
        if names_separate_df["group"].nunique() == len(names_separate_df):
            print(f"\tindex {idx}: ok")
        else:
            print(f"\tindex {idx}: FAILED")
            display(names_separate_df)


def test_in_constraint(in_df, solution_df, verbose=True):
    """
    Test to ensure specified name assigned to specified group.
    """
    if verbose:
        display(in_df)

    for idx, in_row in in_df.iterrows():
        name_in_df = solution_df.loc[solution_df["name"] == in_row["name"]]
        if name_in_df.iloc[0]["group"] == in_row["group id"]:
            print(f"\tindex {idx}: ok")
        else:
            print(f"\tindex {idx}: FAILED")
            display(name_in_df)


def test_not_in_constraint(not_in_df, solution_df, verbose=True):
    """
    Test to ensure specified name not assigned to specified group.
    """
    if verbose:
        display(not_in_df)

    for idx, not_in_row in not_in_df.iterrows():
        name_not_in_df = solution_df.loc[solution_df["name"] == not_in_row["name"]]
        if name_not_in_df.iloc[0]["group"] != not_in_row["group id"]:
            print(f"\tindex {idx}: ok")
        else:
            print(f"\tindex {idx}: FAILED")
            display(name_not_in_df)


def test_homogenous_constraint(hom_df, solution_df, verbose=True):
    """
    Test to ensure all names in specified group have specified characteristic.
    """
    if verbose:
        display(hom_df)

    for idx, hom_row in hom_df.iterrows():
        hom_group_df = solution_df.loc[solution_df["group"] == hom_row["group id"]]
        # get count of names with char value, return 0 if no names with char value
        val_count = hom_group_df[hom_row["characteristic"]].value_counts().to_dict().get(hom_row["value"], 0)
        if  val_count == len(hom_group_df):
            print(f"\tindex {idx}: ok")
        else:
            print(f"\tindex {idx}: FAILED")
            display(hom_group_df)


def test_maximum_constraint(max_df, solution_df, verbose=True):
    """
    Test to ensure no more than maximum number of people with specified characteristic assigned to each group.
    """
    if verbose:
        display(max_df)

    for idx, max_row in max_df.iterrows():
        print(f"\tindex {idx}:")
        for name, group in solution_df.groupby("group"):
            # get count of names with char value, return 0 if no names with char value
            val_count = group[max_row["characteristic"]].value_counts().to_dict().get(max_row["value"], 0)
            if val_count <= max_row["maximum"]:
                print(f"\t\tgroup {name}: ok ({val_count})")
            else:
                print(f"\t\tgroup {name}: FAILED ({val_count} not <= {max_row['maximum']})")


###########################
# Test Multiple Solutions #
###########################

def view_changes_by_group(file, unique_solns, verbose=False):
    """
    View number of changes between one solution and the next displayed by group.

    Example:

    GROUP 1
        solution 0 --> solution 1: 2 of 4
        solution 1 --> solution 2: 3 of 4
        ...
    """
    group_df = import_from_template(file, "Grouping Setup")
    groups = group_df["group id"].to_list()

    # only proceed if multiple solutions...
    if len(unique_solns) > 1:

        for group in groups:
            print(f"\nGROUP {group}")

            for idx in range(len(unique_solns) - 1):
                group_soln_df_0 = unique_solns[idx].loc[unique_solns[idx]["group"] == group]
                group_soln_df_1 = unique_solns[idx + 1].loc[unique_solns[idx + 1]["group"] == group]

                if verbose:
                    if idx == 0:
                        print(f"\nsolution {idx}")
                        display(group_soln_df_0)
                    print(f"\nsolution {idx + 1}")
                    display(group_soln_df_1)

                # names in group_soln_df_0 that are not in group_soln_df_1
                names_changed = set(group_soln_df_0["name"].to_list()) - set(group_soln_df_1["name"].to_list())
                num_changes = len(names_changed)
                print(f"\tsolution {idx} --> solution {idx + 1}: {num_changes} of {len(group_soln_df_0)}")


def view_changes_by_solution(file, unique_solns, verbose=False):
    """
    View number of changes by group between one solution and the next.

    Example:

    SOLUTION 0 --> SOLUTION 1
        group 1: 2
        group 2: 2
        ...
    """
    group_df = import_from_template(file, "Grouping Setup")
    groups = group_df["group id"].to_list()

    for idx in range(len(unique_solns) - 1):
        print(f"\nSOLUTION {idx} --> SOLUTION {idx + 1}")
        soln_df_0 = unique_solns[idx]
        soln_df_1 = unique_solns[idx + 1]
        total_num_changes = 0

        for group in groups:
            group_soln_df_0 = soln_df_0.loc[soln_df_0["group"] == group]
            group_soln_df_1 = soln_df_1.loc[soln_df_1["group"] == group]

            if verbose:
                print(f"\nsolution {idx}")
                display(group_soln_df_0)
                print(f"\nsolution {idx + 1}")
                display(group_soln_df_1)

            # names in group_soln_df_0 that are not in group_soln_df_1
            names_changed = set(group_soln_df_0["name"].to_list()) - set(group_soln_df_1["name"].to_list())
            num_changes = len(names_changed)
            print(f"\t group {group}: {num_changes}")

            total_num_changes += num_changes
        print(f" ==> {total_num_changes} total ({int(100 * (total_num_changes/len(soln_df_0)))}%)")
