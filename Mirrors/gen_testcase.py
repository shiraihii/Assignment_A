#!/usr/bin/env python
# -*- coding: utf-8 -*-

num_row = 1000000
num_col = 1000000
num_mir = 1000


def output_pt(f, x, y):
    f.write("{0} {1}\n".format(x, y))


def output_testcase(f, pts_slash, pts_backslash):
    f.write("{0} {1} {2} {3}\n".format(
        num_row,
        num_col,
        len(pts_slash),
        len(pts_backslash)
    ))
    for pt in pts_slash:
        output_pt(f, *pt)
    for pt in pts_backslash:
        output_pt(f, *pt)


output_filename = 'testcase_1.txt'
f = open(output_filename, 'w')

pts_slash = []
pts_backslash = []
for mir_index in range(num_mir):
    pts_backslash.append([1, mir_index * 2 + 10])
    pts_backslash.append([num_row, mir_index * 2 + 10])
    pts_slash.append([1, mir_index * 2 + 11])
    pts_slash.append([num_row, mir_index * 2 + 11])

    pts_slash.append([10 + mir_index * 2, 1])
    pts_slash.append([10 + mir_index * 2, num_col])
    pts_backslash.append([11 + mir_index * 2, 1])
    pts_backslash.append([11 + mir_index * 2, num_col])

pts_backslash.append([num_row, num_col])

output_testcase(f, pts_slash, pts_backslash)
