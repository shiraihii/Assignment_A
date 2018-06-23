#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from typing import NamedTuple
from scipy import sparse


def parse_input(filename):
    with open(filename) as f:
        is_map_size_read = False
        cnt_case = 0
        for line in f:
            if not is_map_size_read:
                num_row, num_col, num_slash, num_backslash = [
                    int(i) for i in line.split()
                ]
                cnt_case += 1
                is_map_size_read = True
                mirror_pt_r = [-1] * (num_slash + num_backslash)
                mirror_pt_c = [-1] * (num_slash + num_backslash)
                mirror_direction = [0] * (num_slash + num_backslash)
                cnt_mirrot_pt = 0
                if (num_slash + num_backslash == 0):
                    mirrors_solve_empty(cnt_case, num_row, num_col)
                    is_map_size_read = False
            else:
                if (cnt_mirrot_pt <= num_slash + num_backslash - 1):
                    mirror_pt_r[cnt_mirrot_pt], mirror_pt_c[cnt_mirrot_pt] = [
                        int(i) - 1 for i in line.split()
                    ]
                    if (cnt_mirrot_pt < num_slash):
                        # / is +1
                        mirror_direction[cnt_mirrot_pt] = +1
                    else:
                        # \ is -1
                        mirror_direction[cnt_mirrot_pt] = -1

                if (cnt_mirrot_pt == num_slash + num_backslash - 1):
                    mirrors_solve(cnt_case, mirror_direction,
                                  mirror_pt_r, mirror_pt_c, num_row, num_col)
                    is_map_size_read = False
                cnt_mirrot_pt += 1


def mirrors_solve_empty(cnt_case, num_row, num_col):
    if (num_row == 1):
        print("Case {0}: 0".format(cnt_case))
    else:
        print("Case {0}: impossible".format(cnt_case))
    return


def light_forward(light_pos_r, light_pos_c, light_direction):
    if (light_direction == 0):
        return light_pos_r, light_pos_c + 1
    elif (light_direction == 1):
        return light_pos_r - 1, light_pos_c
    elif (light_direction == 2):
        return light_pos_r, light_pos_c - 1
    elif (light_direction == 3):
        return light_pos_r + 1, light_pos_c
    return light_pos_r, light_pos_c


def light_reflect(light_direction, mirror_direction):
    reflection_map = [[3, 2, 1, 0], [1, 0, 3, 2]]
    if (mirror_direction == -1):
        mirror_direction = 0
    return reflection_map[mirror_direction][light_direction]


def is_light_inmap(light_pos_r, light_pos_c, num_row, num_col):
    return 0 <= light_pos_r < num_row and 0 <= light_pos_c < num_col


def mirrors_solve(cnt_case, mirror_direction, mirror_pt_r, mirror_pt_c, num_row, num_col):
    mirror_mat = sparse.coo_matrix(
        (mirror_direction, (mirror_pt_r, mirror_pt_c)), shape=(num_row, num_col)).todok()
    light_mat_forward = sparse.dok_matrix((num_row, num_col), dtype=int)
    light_mat_backward = sparse.dok_matrix((num_row, num_col), dtype=int)
    # Forward Light Calculation
    # Direction 0 ->, 1 Up, 2 <- 3 Down
    light_direction = 0
    light_pos_r, light_pos_c = 0, -1
    while True:
        light_pos_r, light_pos_c = light_forward(
            light_pos_r, light_pos_c, light_direction)
        if (not is_light_inmap(light_pos_r, light_pos_c, num_row, num_col)):
            break
        light_mat_forward[light_pos_r, light_pos_c] = 1
        if (mirror_mat[light_pos_r, light_pos_c] != 0):
            light_direction = light_reflect(
                light_direction, mirror_mat[light_pos_r, light_pos_c])
    # After forward light reached detector
    # Then success and print 0
    if (light_pos_r == num_row - 1 and light_pos_c == num_col):
        return print("Case {0}: 0".format(cnt_case))

    # Backward Light Calculation
    light_direction = 2
    light_pos_r, light_pos_c = num_row - 1, num_col
    while True:
        light_pos_r, light_pos_c = light_forward(
            light_pos_r, light_pos_c, light_direction)
        if (not is_light_inmap(light_pos_r, light_pos_c, num_row, num_col)):
            break
        light_mat_backward[light_pos_r, light_pos_c] = 1
        if (mirror_mat[light_pos_r, light_pos_c] != 0):
            light_direction = light_reflect(
                light_direction, mirror_mat[light_pos_r, light_pos_c])

    # Add light_mat_forward and light_mat_backward
    light_mat_sum = light_mat_forward + light_mat_backward
    # Get solution
    solution_mat = sparse.dok_matrix((num_row, num_col), dtype=bool)
    solution_mat[light_mat_sum == 2] = True
    solution_mat = solution_mat.tocoo()
    solution_num = solution_mat.sum()

    if (solution_num == 0):
        # No solution
        print("Case {0}: impossible".format(cnt_case))
    else:
        # Output Solution
        print("Case {0}: {1} {2} {3}".format(
            cnt_case, solution_num, solution_mat.row[0]+1, solution_mat.col[0]+1))


if __name__ == '__main__':
    # parse command line
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 2):
        print('Usage: python %s filename' % argvs[0])
        quit()
    filename = argvs[1]
    # read input filename
    parse_input(filename)
