from sympy import *
pprint_use_unicode(true)

n = symbols('n', integer=True, positive=True)
m = symbols('m', integer=True, positive=True)
Tx, Ty = symbols('Tx Ty', integer=True, positive=True)
Ax, Ay, Bx, By = symbols('Ax Ay Bx By')
eq1 = Eq(Ax*n + Bx*m, Tx)
eq2 = Eq(Ay*n + By*m, Ty)
print(solve((eq1, eq2), (n, m)))

