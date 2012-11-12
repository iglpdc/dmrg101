## module eigenvals3
''' lam = eigenvals3(d,c,N).
    Returns the N smallest eigenvalues of a
    tridiagonal matrix [A] = [c\d\c].
'''    
import numpy as np
import scipy.optimize
from lamRange import *
from sturmSeq import sturmSeq

def eigenvals3(d,c,N):

    def f(x):             # f(x) = |[A] - x[I]|
        p = sturmSeq(d,c,x)
        return p[len(p)-1]

    evals = np.empty(N)
    r = lamRange(d,c,N)   # Bracket eigenvalues
    for i in range(N):    # Solve by Brent's method
	assert( f(r[i]) * f(r[i+1]) < 0.0 ) 
        evals[i] = scipy.optimize.brentq(f,r[i],r[i+1])
    return evals   
