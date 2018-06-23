#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import numpy
# Numpy for binary search on sorted list


def parse_input(filename):
    with open(filename) as f:
        is_map_size_read = False
        cnt_case = 0
        for line in f:
            if not is_map_size_read:
                # Read a new safe-map
                num_row, num_col, num_slash, num_backslash = [
                    int(i) for i in line.split()
                ]
                # Add 2 virtual columns to left and right
                num_col += 2
                cnt_case += 1
                is_map_size_read = True
                # Initialize list of mirror point
                mirror_pt_r = [-1] * (num_slash + num_backslash + 2)
                mirror_pt_c = [-1] * (num_slash + num_backslash + 2)
                mirror_pt_dir = [0] * (num_slash + num_backslash + 2)
                cnt_mirrot_pt = 0
                # If none mirror exist
                if (num_slash + num_backslash == 0):
                    # Directly solve by size of safe-map
                    mirrors_solve_empty(cnt_case, num_row, num_col)
                    # Ready for next case
                    is_map_size_read = False

            else:
                if (cnt_mirrot_pt <= num_slash + num_backslash - 1):
                    if (cnt_mirrot_pt < num_slash):
                        # / mirror
                        mirror_pt_r[cnt_mirrot_pt] = \
                            int(line.split()[0]) - 1
                        mirror_pt_c[cnt_mirrot_pt] = \
                            int(line.split()[1])
                        # Mark mirror polarity
                        mirror_pt_dir[cnt_mirrot_pt] = 1
                    else:
                        # \ mirror
                        mirror_pt_r[cnt_mirrot_pt] = \
                            int(line.split()[0]) - 1
                        mirror_pt_c[cnt_mirrot_pt] = \
                            int(line.split()[1])
                if (cnt_mirrot_pt == num_slash + num_backslash - 1):
                    # Add virtual mirror of emitter and receiver
                    # Left-top emitter
                    mirror_pt_r[-2] = 0
                    mirror_pt_c[-2] = 0
                    # Right-bottom receiver
                    mirror_pt_r[-1] = num_row - 1
                    mirror_pt_c[-1] = num_col - 1
                    # Solve case
                    mirrors_solve(cnt_case, mirror_pt_r, mirror_pt_c,
                                  mirror_pt_dir, num_row, num_col)
                    # Ready for next case
                    is_map_size_read = False
                cnt_mirrot_pt += 1


def mirrors_solve_empty(cnt_case, num_row, num_col):
    # Available only when number of row is 1
    if (num_row == 1):
        print("Case {0}: 0".format(cnt_case))
    # Otherwise impossible
    else:
        print("Case {0}: impossible".format(cnt_case))
    return


def cal_light(r, c, d, mat_csr, mat_csc, num_row, num_col):
    # Calculate Light Beam
    # Para:
    #   r, c: initial row_index, initial terminal
    #   d: initial direction, 0 for Right, 1 for Up, 2 for Left, 3 for Down
    #   mat_csr, mat_csc: dict
    #       compress sparse matrix of map in list of row / column, respectively
    #       every row / column is stored corresponding index
    #       and 0rd entry is a every list of column / row index of mirrors
    #       and 1st entry is pair of (column / row index, mirror_polarity)
    #           mirror_polarity, 0 for \, 1 for /
    #       mat_csr Example of Testcase 1
    #       {
    #           0: [[0, 2],     [[0, 0], [2, 0]]],
    #           1: [[3, 5],     [[3, 1], [5, 0]]],
    #           3: [[2],        [[2, 0]]],
    #           4: [[5, 7],     [[5, 0], [7, 0]]]
    #       }
    #   num_row, num_col: number of row, number of column

    # Return: r, c, light_h, light_v
    #   r, c: terminal row_index, terminal column_index
    #   light_h: list
    #       with entry [row_index, column_start_index, column_end_index] of horizontal light beam
    #   light_v: list(SORTED by column_index)
    #       with entry [column_index, row_start_index, row_end_index] of vertical light beam

    # Initialization
    found = True
    light_h = []
    light_v = []
    while found:
        # Find next mirror point or wall point
        found, next_r, next_c, next_d = find_next_mirror(
            r, c, d, mat_csr, mat_csc, num_row, num_col)
        # Add light beam to light list
        if (d == 0):
            # Horizontal Right
            light_h.append([r, c, next_c])
        elif (d == 2):
            # Horizontal Left
            light_h.append([r, next_c, c])
        elif (d == 3):
            # Vertical Down
            light_v.append([c, r, next_r])
        else:
            # Vertical Up
            light_v.append([c, next_r, r])
        r, c, d = next_r, next_c, next_d
    # Sorted vertical light
    light_v.sort()
    return r, c, light_h, light_v


def find_next_mirror(r, c, d, mat_csr, mat_csc, num_row, num_col):
    # Mapping of direction after a mirror
    reflection_map = [[3, 2, 1, 0], [1, 0, 3, 2]]
    # Find current position's mirror
    if (d == 0 or d == 2):
        # Light is horizontal
        # Find current position's mirror in csr
        index = numpy.searchsorted(mat_csr[r][0], c)
        # Find next mirror's position
        index += (1 if d == 0 else -1)
        # If no mirror, then set to wall's position
        if index < 0 or index >= len(mat_csr[r][0]):
            c = num_col - 1 if d == 0 else 0
            return False, r, c, d
        else:
            # Get next mirror's polarity
            m_pol = mat_csr[r][1][index][1]
            c = mat_csr[r][1][index][0]
            d = reflection_map[m_pol][d]
            return True, r, c, d
    else:
        # Light is vertical
        # Find current position's mirror in csr
        index = numpy.searchsorted(mat_csc[c][0], r)
        # Find next mirror's position
        index += (1 if d == 3 else -1)
        # If no mirror, then set to wall's position
        if index < 0 or index >= len(mat_csc[c][0]):
            r = num_row - 1 if d == 3 else 0
            return False, r, c, d
        else:
            # Get next mirror's polarity
            m_pol = mat_csc[c][1][index][1]
            r = mat_csc[c][1][index][0]
            d = reflection_map[m_pol][d]
            return True, r, c, d


def mirrors_solve(cnt_case, mirror_pt_r, mirror_pt_c, mirror_pt_dir, num_row, num_col):
    # Initlize mat_csr nad mst_csc
    # Format detail in comment of function 'cal_light'
    mat_csr = {}
    mat_csc = {}
    for r, c, d in zip(mirror_pt_r, mirror_pt_c, mirror_pt_dir):
        if r in mat_csr:
            mat_csr[r][0].append(c)
            mat_csr[r][1].append([c, d])
        else:
            mat_csr[r] = [[c], [[c, d]]]
        if c in mat_csc:
            mat_csc[c][0].append(r)
            mat_csc[c][1].append([r, d])
        else:
            mat_csc[c] = [[r], [[r, d]]]
    for k in mat_csr:
        mat_csr[k][0].sort()
        mat_csr[k][1].sort()
    for k in mat_csc:
        mat_csc[k][0].sort()
        mat_csc[k][1].sort()

    # Forwarding light from left-top's emitter
    r, c, light_forward_h, light_forward_v = cal_light(
        0, 0, 0, mat_csr, mat_csc, num_row, num_col)
    # If the final position is bottom
    # Meaning the safe available without adding a mirror
    if (r == num_row - 1 and c == num_col - 1):
        return print("Case {0}: 0".format(cnt_case))
    # If not
    # Backwarding light from right-bottom's receiver
    r, c, light_backward_h, light_backward_v = cal_light(
        num_row - 1, num_col - 1, 2, mat_csr, mat_csc, num_row, num_col)

    # Fasten intersection point calculation
    light_forward_v_indices = [x[0] for x in light_forward_v]
    light_backward_v_indices = [x[0] for x in light_backward_v]
    solutions_num = 0
    solution = [num_row + 2, num_col + 2]
    # For forward light beam's horizontal
    for [r, col_start, col_end] in light_forward_h:
        # Find indices of possible intersection
        index_start = numpy.searchsorted(light_backward_v_indices, col_start)
        index_end = numpy.searchsorted(light_backward_v_indices, col_end)
        if (index_end < len(light_backward_v_indices)):
            if (light_backward_v_indices[index_end] == col_end):
                index_end += 1
        # Try to find intersection
        for [c, row_start, row_end] in light_backward_v[index_start:index_end]:
            if (row_start <= r <= row_end):
                # If Found
                solutions_num += 1
                if (solution > [r, c]):
                    # Update best solution
                    solution = [r, c]
    # Same for backward's
    for [r, col_start, col_end] in light_backward_h:
        index_start = numpy.searchsorted(light_forward_v_indices, col_start)
        index_end = numpy.searchsorted(light_forward_v_indices, col_end)
        if (index_end < len(light_forward_v_indices)):
            if (light_forward_v_indices[index_end] == col_end):
                index_end += 1
        for [c, row_start, row_end] in light_forward_v[index_start:index_end]:
            if (row_start <= r <= row_end):
                solutions_num += 1
                if (solution > [r, c]):
                    solution = [r, c]

    if (solutions_num == 0):
        # No solution
        print("Case {0}: impossible".format(cnt_case))
    else:
        # Output Solution
        print("Case {0}: {1} {2} {3}".format(
            cnt_case, solutions_num,
            # Since the problem indicate the first row/column's index as 1 rather than 0
            # Don't forget we have add a virtual column to both left and right
            # So don't need to add 1 to the column index
            solution[0] + 1, solution[1])
        )


if __name__ == '__main__':
    # Parse command line
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 2):
        print('Usage: python %s filename' % argvs[0])
        quit()
    filename = argvs[1]
    # Run
    parse_input(filename)
