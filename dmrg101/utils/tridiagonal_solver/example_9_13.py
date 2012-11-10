#!/usr/bin/env python
from numpy import ones 
from lamRange import *
from inversePower3 import *
N = 100
n = 100
d = ones((n))*2.0
c = ones((n-1))*(-1.0)
r = lamRange(d,c,N)
print r
for i in range(1, len(r)):
    s = (r[i-1] + r[i])/2.0
    print s
#    lam,x = inversePower3(d,c,s) # Inverse power method 
#    print "Eigenvalue No." , i, " =",lam
#    #print "Eigenvec No." , i, " =",x
