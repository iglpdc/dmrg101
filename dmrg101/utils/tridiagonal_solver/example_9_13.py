#!/usr/bin/env python
from numpy import ones 
from tridiagonal_solver import *
n = 300
d = ones((n))*2.0
c = ones((n-1))*(-1.0)

evals, evecs = tridiagonal_solver(d,c) 
print evals
print evecs
