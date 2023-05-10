import time
from grid import Grid
from plot_results import PlotResults

def ac3(grid, var):
    """
        This is a domain-specific implementation of AC3 for Sudoku. 

        It keeps a set of arcs to be processed (arcs) which is provided as input to the method. 
        Since this is a domain-specific implementation, we don't need to maintain a graph and a set 
        of arcs in memory. We can store in arcs the cells of the grid and, when processing a cell, 
        we ensure arc consistency of all variables related to this cell by removing the value of
        cell from all variables in its column, row, and unit. 

        For example, if the method is used as a preprocessing step, then arcs is initialized with 
        all cells that start with a number on the grid. This method ensures arc consistency by
        removing from the domain of all variables in the row, column and unit the values of 
        the cells given as input. The method adds to the set of arcs all variables that have
        their values assigned during the propagation of the contrains. 
    """
    if not type(var) == list:
        arcs = [var]
    else:
        arcs = var
    checked = set()
    while len(arcs):
        cell = arcs.pop()
        checked.add(cell)

        assigned_row, failure = grid.remove_domain_row(cell[0], cell[1])
        if failure: return failure

        assigned_column, failure = grid.remove_domain_column(cell[0], cell[1])
        if failure: return failure

        assigned_unit, failure = grid.remove_domain_unit(cell[0], cell[1])
        if failure: return failure

        arcs.extend(assigned_row)
        arcs.extend(assigned_column)
        arcs.extend(assigned_unit)    
    return False

def pre_process_ac3(grid):
    """
    This method enforces arc consistency for the initial grid of the puzzle.

    The method runs AC3 for the arcs involving the variables whose values are 
    already assigned in the initial grid. 
    """
    arcs_to_make_consistent = []

    for i in range(grid.get_width()):
        for j in range(grid.get_width()):
            if len(grid.get_cells()[i][j]) == 1:
                arcs_to_make_consistent.append((i, j))

    ac3(grid, arcs_to_make_consistent)

def select_variable_fa(grid):
    for i in range(grid.get_width()):
        for j in range(grid.get_width()):
            if len(grid.get_cells()[i][j]) > 1:
                return tuple([i, j])
    return None

def select_variable_mrv(grid):
    min_len = 10
    min_var = []

    for i in range(grid.get_width()):
        for j in range(grid.get_width()):
            if len(grid.get_cells()[i][j]) <= min_len and len(grid.get_cells()[i][j]) > 1:
                min_len = len(grid.get_cells()[i][j])
                min_var.append(tuple([i, j]))

    return min_var[-1]

def search(grid, var_selector):

    if grid.is_solved():
        # grid.print()
        return grid
    var = var_selector(grid)

    for d in grid.get_cells()[var[0]][var[1]]:
        if grid.is_value_consistent(d,var[0], var[1]):

            copy_grid = grid.copy()
            copy_grid.get_cells()[var[0]][var[1]] = d
            result = search(copy_grid, var_selector)
            if result is not None:
                return result

    return None

def backtracking_ac3(grid, var_selector):

    if grid.is_solved():
        grid.print()
        return grid

    var = var_selector(grid)

    for d in grid.get_cells()[var[0]][var[1]]:
        # if check_consistency_row(grid, var[0], var[1], d) and check_consistency_column(grid, var[0], var[1], d) \
        #         and check_consistency_3x3(grid, var[0], var[1], d):
        if grid.is_value_consistent(d, var[0], var[1]):
            copy_grid = grid.copy()
            copy_grid.get_cells()[var[0]][var[1]] = d
            ri = ac3(copy_grid, var)

            if not ri:
                # pre_process_ac3(copy_grid)
                result = backtracking_ac3(copy_grid, var_selector)
                if result is not None:
                    return result

    return None

file = open('tutorial_problem.txt', 'r')
problems = file.readlines()
for p in problems:
    g = Grid()
    g.read_file(p)
    k = Grid()
    k.read_file(p)
    # test your backtracking implementation without inference here
    fa_test = search(g, select_variable_fa)
    mrv_test = search(k, select_variable_mrv)
    # this test instance is only meant to help you debug your backtracking code
    # once you have implemented forward checking, it is fine to find a solution to this instance with inference
    fa_test.print()
    mrv_test.print()
file = open('top95.txt', 'r')
problems = file.readlines()


# running_time_mrv = []
# running_time_fa = []
#
for p in problems:
    g = Grid()
    h = Grid()

    g.read_file(p)
    h.read_file(p)

    # start_fa = time.time()
    pre_process_ac3(g)
    backtracking_ac3(g, select_variable_fa)
    # end_fa = time.time()
    # running_time_fa.append(end_fa - start_fa)

    # start_mrv = time.time()
    pre_process_ac3(h)
    backtracking_ac3(h, select_variable_mrv)
    # end_mrv = time.time()
    # running_time_mrv.append(end_mrv - start_mrv)

# plotter = PlotResults()
# plotter.plot_results(running_time_mrv, running_time_fa, "Running Time Backtracking (MRV)", "Running Time Backtracking (FA)", "running time")

    # test your backtracking implementation with inference here for instance grid_copy