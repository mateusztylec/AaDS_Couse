#!/usr/bin/python
# -*- coding: utf-8 -*-
# import numpy as np
#
# M = np.empty((0, 1))
# M = np.append(M, np.array([[None]]), axis=0)
# print(M[0][0])
# M = np.append(M, np.array([[None]]), axis=0)
# M = np.append(M, np.array([[None], [1]]), axis=1)
# M = np.append(M, np.array([[None, None]]), axis=0)
# M[0] = None
# M[1] = None
# M[2] = None
# M[0][0] = None
#
# print(M)
#

unused = ['a','b','c','d']

for i in unused:
    to_remember = unused.pop(0)
    print(i)