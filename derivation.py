'''The following is a symbolic derivation of the functions
tokensToEthereum_ and ethereumToTokens_
in the PoWH3D contract.
See https://osolmaz.com/2018/08/03/token-bonding-1/'''

from sympy import *

S = Symbol('S')
S0 = Symbol('S_0')
E = Symbol('E')
T = Symbol('T')

P0 = sympify('P_0')
Ip = sympify('I_p')

P = P0 + S*Ip

print('Purchase')

E_calc = integrate(P, (S, S0, S0+T))
E_calc = simplify(E_calc)
E_calc = E_calc.subs(S0, S)
# pprint(E_calc)

T_calc = solve(E - E_calc, T)[0]
T_calc = T_calc.subs(S0, S)
pprint(T_calc)

print('Sale')

E_calc = integrate(P, (S, S0-T, S0))
E_calc = simplify(E_calc)
E_calc = E_calc.subs(S0, S)
pprint(E_calc)

# T_calc = solve(E - E_calc, T)[0]
# T_calc = T_calc.subs(S0, S)
# pprint(T_calc)

