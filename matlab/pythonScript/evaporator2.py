import math

import numpy as np
from scipy import integrate
# import matplotlib.pyplot as plt
import sympy


def apply_ics(sol, ics, x, known_params):
    """
    Apply the initial conditions (ics), given as a dictionary on
    the form ics = {y(0): y0, y(x).diff(x).subs(x, 0): yp0, ...},
    to the solution of the ODE with independent variable x.
    The undetermined integration constants C1, C2, ... are extracted
    from the free symbols of the ODE solution, excluding symbols in
    the known_params list.
    """

    free_params = sol.free_symbols - set(known_params)
    ## free parameters like C1,C2, that needed to be figured out with ics and boundary conditions
    eqs = [(sol.lhs.diff(x, n) - sol.rhs.diff(x, n)).subs(x, 0).subs(ics) for n in range(len(ics))]
    ## form equations with general solution(sol), by substituting the x with 0 and [y(0),dy/dx(x=0)...] with ics.
    sol_params = sympy.solve(eqs, free_params)
    ## solve the algebraic equation set  to get the free parameters expression
    ## return the solution after substituting the free parameters

    return sol.subs(sol_params)


# tew1=12
# m1=5.574
# Cpw=4.187
# Gew=1.05
# Qe=450


sympy.init_printing()
## initialize the print environment
tao, tew1, m2, Cpw, Gc, Qc = sympy.symbols("tao, tew1, m2, Cpw, Gc, Qc", positive=True)
## symbolize the parameters and they can only be positive
tew2 = sympy.Function('tew2')
## set x to be the differential function, not the variable
ode = 0.5 * m2 * Cpw * (tew2(tao).diff(tao, 1)) - Qc + Gc * Cpw * (tew2(tao) - tew1)
ode_sol = sympy.dsolve(ode)
## use diff() and dsolve to get the general solution
ics = {tew2(0): -15}
## apply dict to the initial conditions
x_t_sol = apply_ics(ode_sol, ics, tao, [tao, tew1, m2, Cpw, Gc, Qc])
## get the solution with ics by calling function apply_ics.
sympy.pprint(x_t_sol)
## pretty print
## solution is as follows


tew1_const = 35
m2_const = 7.016
Cpw_const = 4.187
Gc_const = 1.2
Qc_const = 600

tao_const = 0;
#
output = tew1_const + Qc_const / (Cpw_const * Gc_const) + (
        -Cpw_const * Gc_const * tew1_const -15 * Cpw_const * Gc_const - Qc_const) * (
             pow(2.71828, (-2 * Gc_const * tao_const) / (m2_const))) / (Cpw_const * Gc_const)

print(output)
