#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import numpy


def parse_input(filename):
    with open(filename) as f:
        is_map_size_read = False
        cnt_case = 0
        for line in f:
            if not is_map_size_read:
                num_row, num_col, num_slash, num_backslash = [
                    int(i) for i in line.split()
                ]
                num_col += 2
                cnt_case += 1
                is_map_size_read = True
                mirror_pt_r = [-1] * (num_slash + num_backslash + 2)
                mirror_pt_c = [-1] * (num_slash + num_backslash + 2)
                mirror_pt_dir = [0] * (num_slash + num_backslash + 2)
                cnt_mirrot_pt = 0
                if (num_slash + num_backslash == 0):
                    mirrors_solve_empty(cnt_case, num_row, num_col)
                    is_map_size_read = False

            else:
                if (cnt_mirrot_pt <= num_slash + num_backslash - 1):
                    if (cnt_mirrot_pt < num_slash):
                        # /
                        mirror_pt_r[cnt_mirrot_pt] = \
                            int(line.split()[0]) - 1
                        mirror_pt_c[cnt_mirrot_pt] = \
                            int(line.split()[1])
                        mirror_pt_dir[cnt_mirrot_pt] = 1
                    else:
                        # \
                        mirror_pt_r[cnt_mirrot_pt] = \
                            int(line.split()[0]) - 1
                        mirror_pt_c[cnt_mirrot_pt] = \
                            int(line.split()[1])
                if (cnt_mirrot_pt == num_slash + num_backslash - 1):
                    # Add Virtual Initial and Tail Mirror(backslash)
                    mirror_pt_r[-2] = 0
                    mirror_pt_c[-2] = 0
                    mirror_pt_r[-1] = num_row - 1
                    mirror_pt_c[-1] = num_col - 1
                    mirrors_solve(cnt_case, mirror_pt_r, mirror_pt_c,
                                  mirror_pt_dir, num_row, num_col)
                    is_map_size_read = False
                cnt_mirrot_pt += 1


def mirrors_solve_empty(cnt_case, num_row, num_col):
    if (num_row == 1):
        print("Case {0}: 0".format(cnt_case))
    else:
        print("Case {0}: impossible".format(cnt_case))
    return


def cal_light(r, c, d, light_bundle, mat_csr, mat_csc, num_row, num_col):
    found = True
    while found:
        found, next_r, next_c, next_d = find_next_mirror(
            r, c, d, mat_csr, mat_csc, num_row, num_col)
        if (d == 0):
            # Horizontal Right
            light_bundle[0][r] = [c, next_c]
        elif (d == 2):
            # Horizontal Left
            light_bundle[0][r] = [next_c, c]
        elif (d == 3):
            # Vertical Down
            light_bundle[1][c] = [r, next_r]
        else:
            # Vertical Up
            light_bundle[1][c] = [next_r, r]
        r, c, d = next_r, next_c, next_d
    return r, c, d


def find_next_mirror(r, c, d, mat_csr, mat_csc, num_row, num_col):
    # mapping of direction after a mirror
    reflection_map = [[3, 2, 1, 0], [1, 0, 3, 2]]
    # find current position's mirror
    if (d == 0 or d == 2):
        # Light is horizontal
        # Find Current position's mirror in csr
        index = numpy.apply_along_axis(
            lambda a: a.searchsorted(c), axis=0, arr=mat_csr[r])[0]

        # Find Next
        index += (1 if d == 0 else -1)
        if index < 0 or index >= len(mat_csr[r]):
            c = num_col - 1 if d == 0 else 0
            return False, r, c, d
        else:
            m_pol = mat_csr[r][index][1]
            c = mat_csr[r][index][0]
            d = reflection_map[m_pol][d]
            return True, r, c, d
    else:
        # Light is vertical
        # Find Current position's mirror in csc
        index = numpy.apply_along_axis(
            lambda a: a.searchsorted(r), axis=0, arr=mat_csc[c])[0]
        # Find Next
        index += (1 if d == 3 else -1)
        if index < 0 or index >= len(mat_csc[c]):
            r = num_row - 1 if d == 3 else 0
            return False, r, c, d
        else:
            m_pol = mat_csc[c][index][1]
            r = mat_csc[c][index][0]
            d = reflection_map[m_pol][d]
            return True, r, c, d


def mirrors_solve(cnt_case, mirror_pt_r, mirror_pt_c, mirror_pt_dir, num_row, num_col):
    mat_csr = {}
    mat_csc = {}
    for r, c, d in zip(mirror_pt_r, mirror_pt_c, mirror_pt_dir):
        if r in mat_csr:
            mat_csr[r].append([c, d])
        else:
            mat_csr[r] = [[c, d]]
        if c in mat_csc:
            mat_csc[c].append([r, d])
        else:
            mat_csc[c] = [[r, d]]
    for k in mat_csr:
        mat_csr[k].sort()
    for k in mat_csc:
        mat_csc[k].sort()

    # light_bundle
    # [horizontal_lights, vertical_lights]
    light_bundle_forward = [{}, {}]
    light_bundle_backward = [{}, {}]
    r, c, d = cal_light(0, 0, 0, light_bundle_forward,
                        mat_csr, mat_csc, num_row, num_col)
    if (r == num_row - 1 and c == num_col - 1):
        return print("Case {0}: 0".format(cnt_case))

    cal_light(num_row - 1, num_col - 1, 2, light_bundle_backward,
              mat_csr, mat_csc, num_row, num_col)

    solution = []
    for r in light_bundle_forward[0]:
        [col_start, col_end] = light_bundle_forward[0][r]
        for c in light_bundle_backward[1]:
            [row_start, row_end] = light_bundle_backward[1][c]
            if (row_start < r < row_end) and (col_start < c < col_end):
                solution.append([r, c])

    for r in light_bundle_backward[0]:
        [col_start, col_end] = light_bundle_backward[0][r]
        for c in light_bundle_forward[1]:
            [row_start, row_end] = light_bundle_forward[1][c]
            if row_start <= r <= row_end and col_start <= c <= col_end:
                solution.append([r, c])

    solution.sort()

    if (len(solution) == 0):
        # No solution
        print("Case {0}: impossible".format(cnt_case))
    else:
        # Output Solution
        solution.sort()
        print("Case {0}: {1} {2} {3}".format(
            cnt_case, len(solution), solution[0][0] + 1, solution[0][1]))


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
