import pandas as pd
import pulp
import random


####################
# Helper Functions #
####################

def import_from_template(file, sheet):
    """
    Import data from template .xlsx file. Exclude one-row header.
    """
    return pd.read_excel(file, sheet_name=sheet, header=1)


def create_name_group_tups(file):
    """
    Create list of possible (name, group) combinations.
    """
    person_df = import_from_template(file, "Person Setup")
    names = person_df["name"].to_list()

    group_df = import_from_template(file, "Grouping Setup")
    groups = group_df["group id"].to_list()

    name_group_tups = [(name, group) for name in names for group in groups]

    return name_group_tups


def extract_names_groups_from_d_vars(d_vars):
    """
    Create list of unique names and groups from the decision variables where each decision variable is formatted as a dict with key (name, group) and value "Decision_Variable_(name, _group)".
    """
    names = []
    groups = []
    for name, group in d_vars.keys():
        if name not in names:
            names.append(name)
        if group not in groups:
            groups.append(group)
    return names, groups


def create_groups_size_dict(group_df):
    """
    Create dict of group sizes with {group id: size}.
    """
    return pd.Series(group_df["size"].values, index=group_df["group id"]).to_dict()


########################
# LP Problem Functions #
########################

def setup_lp_problem(var_tups):
    """
    Instantiate LP problem with decision variables and arbitrary objective function (arbitrary because primary objective to meet constraints rather than min/max/etc. a function).
    """
    prob = pulp.LpProblem("Problem", pulp.LpMinimize)
    d_vars = pulp.LpVariable.dicts("Decision Variable", var_tups, cat='Binary')
    # arbitrary objective function
    prob += 0
    return prob, d_vars


def one_group_per_name_constraint(prob, d_vars, names, groups):
    """
    Add constraint to ensure one group assignment per name.
    """
    for name in names:
        prob += sum(d_vars[(name, group)] for group in groups) == 1
    return prob


def max_name_per_group_constraint(prob, d_vars, names, groups, file, sheet="Grouping Setup"):
    """
    Add constraint to ensure no more than maximum number of names assigned to each group.
    """
    group_df = import_from_template(file, sheet)
    groups_size_dict = create_groups_size_dict(group_df)
    for group in groups:
        prob += sum(d_vars[(name, group)] for name in names) <= groups_size_dict[group]
    return prob


def with_constraint(prob, d_vars, groups, file, sheet="Constraint - With"):
    """
    Add constraint to ensure specified names assigned to group together.
    """
    with_df = import_from_template(file, sheet)
    for idx, names_together_row in with_df.iterrows():
        names_together = list(names_together_row.dropna().values)
        for group in groups:
            for idx in range(0, len(names_together)-1):
                prob += d_vars[(names_together[idx], group)] == d_vars[(names_together[idx+1], group)]
    return prob


def not_with_constraint(prob, d_vars, groups, file, sheet="Constraint - Not With"):
    """
    Add constraint to ensure specified names assigned to different groups.
    """
    not_with_df = import_from_template(file, sheet)
    for idx, names_separate_row in not_with_df.iterrows():
        names_separate = list(names_separate_row.dropna().values)
        for group in groups:
            # no more than one of each specified name per group
            prob += sum(d_vars[(name, group)] for name in names_separate) <= 1
    return prob


def in_constraint(prob, d_vars, file, sheet="Constraint - In"):
    """
    Add constraint to ensure specified name assigned to specified group.
    """
    in_df = import_from_template(file, sheet)
    for idx, in_row in in_df.iterrows():
        prob += d_vars[(in_row["name"], in_row["group id"])] == 1
    return prob


def not_in_constraint(prob, d_vars, file, sheet="Constraint - Not In"):
    """
    Add constraint to ensure specified name not assigned to specified group.
    """
    not_in_df = import_from_template(file, sheet)
    for idx, not_in_row in not_in_df.iterrows():
        prob += d_vars[(not_in_row["name"], not_in_row["group id"])] == 0
    return prob


def homogenous_constraint(prob, d_vars, file, sheet="Constraint - Homogenous"):
    """
    Add constraint to ensure all names in specified group have specified characteristic.
    """
    person_df = import_from_template(file, "Person Setup")
    hom_df = import_from_template(file, sheet)
    for idx, hom_row in hom_df.iterrows():
        person_without_char_df = person_df.loc[person_df[hom_row["characteristic"]] != hom_row["value"]]
        names_without_char = person_without_char_df["name"].to_list()
        # exclude names without char from specified group
        for name in names_without_char:
            prob += d_vars[(name, hom_row["group id"])] == 0
    return prob


def max_char_constraint(prob, d_vars, groups, file, elastic, sheet="Constraint - Maximum"):
    """
    Add rigid or elastic maximum characterstic constraint based on elastic parameter. Constraint ensures or encourages no more than the maximum number of people with specified characteristic assigned to each group. With elastic constraint, allow maximum number to relax to zero to ensure the feasibility of the problem.
    """
    person_df = import_from_template(file, "Person Setup")
    max_df = import_from_template(file, sheet)
    for idx, max_row in max_df.iterrows():
        person_with_char_df = person_df.loc[person_df[max_row["characteristic"]] == max_row["value"]]
        names_with_char = person_with_char_df["name"].to_list()
        for group in groups:
            if elastic:
                constraint_lhs = sum(d_vars[(name, group)] for name in names_with_char)
                constraint_rhs = max_row["maximum"]
                # sense value -1 means less than or equal to (<=)
                constraint = pulp.LpConstraint(constraint_lhs, sense=-1, name=int(1000000 * random.random()), rhs=constraint_rhs)
                # penalty-free target interval of 100% on left and 0% on right side of the rhs value ==> [0, constraint_rhs]
                e_constraint = constraint.makeElasticSubProblem(penalty=1, proportionFreeBoundList=[1, 0])
                prob.extend(e_constraint)
            else:
                prob += sum(d_vars[(name, group)] for name in names_with_char) <= max_row["maximum"]
    return prob


def add_constraints(prob, d_vars, file, elastic_max_char_constraint):
    """
    Add all constraints to LP problem.
    """

    names, groups = extract_names_groups_from_d_vars(d_vars)

    prob = one_group_per_name_constraint(prob, d_vars, names, groups)
    prob = max_name_per_group_constraint(prob, d_vars, names, groups, file)
    prob = with_constraint(prob, d_vars, groups, file)
    prob = not_with_constraint(prob, d_vars, groups, file)
    prob = in_constraint(prob, d_vars, file)
    prob = not_in_constraint(prob, d_vars, file)
    prob = homogenous_constraint(prob, d_vars, file)
    prob = max_char_constraint(prob, d_vars, groups, file, elastic_max_char_constraint)

    return prob


def solve_lp_problem(prob, d_vars):
    """
    Solve the LP problem and create solution DataFrame with names and assigned groups.
    """
    prob.solve()
    status = pulp.LpStatus[prob.status]
    # d_vars as dict with {(name, group): "Decision_Variable_(name, _group)"}
    soln_name_group_tups = [k for k, v in list(d_vars.items()) if v.varValue == 1.0]
    solution_df = pd.DataFrame(soln_name_group_tups, columns=["name", "group"])
    return status, solution_df


def run_lp_problem(file, elastic, unique_solutions):
    """
    Setup and solve the LP problem with a rigid or elastic maximum characteristic constraint based on elastic parameter.
    """
    var_tups = create_name_group_tups(file)
    prob, d_vars = setup_lp_problem(var_tups)
    prob = add_constraints(prob, d_vars, file, elastic_max_char_constraint=elastic)
    prob = add_unique_solution_constraint(prob, d_vars, unique_solutions)
    status, solution_df = solve_lp_problem(prob, d_vars)
    return status, solution_df


###############################
# Multiple Solution Functions #
###############################

def add_unique_solution_constraint(prob, d_vars, unique_solutions):
    """
    Add elastic constraint to penalize repeat student assignments. Encourages group assignments to change between solutions.
    """
    if unique_solutions:
        for solution_df in unique_solutions:
            solution_d_vars = [d_vars[(row["name"], row["group"])] for idx, row in solution_df.iterrows()]
            # sense value -1 means less than or equal to (<=)
            # encourage no repeat student assignments
            constraint = pulp.LpConstraint(sum(solution_d_vars), sense=-1, name=int(1000000 * random.random()), rhs=0)
            # penalty-free target interval of 0% on either side of rhs (0)
            # penalize repeat student assignments
            e_constraint = constraint.makeElasticSubProblem(penalty=1, proportionFreeBound=0)
            prob.extend(e_constraint)
    return prob