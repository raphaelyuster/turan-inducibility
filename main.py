# A script for computing the inducibility of complete equipartite graphs (a.k.a. Turan graphs)

# Denote the Tur\'an graph by T(s,r) where s is the number of vertices, r is the number of parts, and 2 <= r < s.
# Let floor [s/r] = p and let s mod r  = q, then there are q parts of size p+1 and r-q parts of size p.
#
# If s=r then the graph is complete and the inducibility is 1.
# Otherwise, the inducibility is obtained by balanced complete l-partite graphon.
# If s=3 and r=2, then l=2 [0]
# If r=2 and s >= 4 (bipartite), then l=2 [1].
# if (1+1/r)^s(1-s/p(r+1)) > 1 then l=r [1].
# if s=5 and r=3 then l=3 can also be derived from [1] (see also [5])
# If s=4 and r=3, then l=5 [2].
# If s=5 and r=4, then l=8 [3,4].
# More generally, if s=r+1, then l is determined in [4].
# Otherwise, if p<= 2 or if (p,q)=(3,0), or (p,q)=(3,1), then r is determined in [6].
#
# References:
# [0] Goodman, "On sets of acquaintances and strangers at any party".
# [1] Brown and Sidorenko, "The inducibility of complete bipartite graphs".
# [2] Hirst, "The inducibility of graphs on four vertices".
# [3] Liu, Pikhurko, Sharifzadeh, Staden, "Stability from graph symmetrisation arguments with applications to inducibility".
# [4] Liu, Mubayi, Reiher,  "The feasible region of induced graphs".
# [5] Pikhurko, Sliacan, Tyros, "Strong Forms of Stability from Flag Algebra Calculations".
# [6] The author.

# Reference key variables for LaTeX table generation

ref0 = "\cite{goodman-1959}"
ref1 = "\cite{BS-1994}"
ref2 = "\cite{hirst-2014}"
ref3 = "\cite{LPSS-2023}"
ref4 = "\cite{LMR-2023}"
ref5 = "\cite{PST-2019}"
ref6 = "here"


# a utility function for gcd
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# a utility function for factorial
def fact(j):
    r = 1
    for i in range(j):
        r = r * (i + 1)
    return r


# computing the numerator of the inducibility
def numerator(l, r, q, p):
    return fact(l) * fact(p * r + q)


# computing the denominator of the inducibility
def denominator(l, r, q, p):
    res = fact(r - q) * fact(q) * fact(l - r) * pow(l, p * r + q)
    return res * pow(p+1,q)*pow(fact(p),r)


# compute f(l) as defined in the paper: f(l)=(1-1/l)^{pr+q}*l/(l-r)
def f(l, r, q, p):
    res = 1
    for i in range(p * r + q):
        res *= 1 - 1 / l
    return res * l / (l - r)


# search for largest l such that f(l) > 1
def search(r, q, p):
    l = r
    while f(l + 1, r, q, p) > 1:
        l += 1
    return l


# Main program. Determine the inducibility of T(s,r) where s > r (T(s,s)=K_s is trivial)
latex = True
if latex:
    print("graph & $t$ & numerator & denominator & reference", end="")
for s in range(3, 15):
    for r in range(2, s):
        p = s // r
        q = s % r
        if r == 2:
            num = fact(2 * p + q) // fact(p) // fact(p + q)
            den = pow(2, 2 * p)
            gc = gcd(num, den)
            num = num // gc
            den = den // gc
            if latex and s == 3:
                print("\\\\\n\\hline\n$T(3,2)$ & $2$ & $" + str(num) + "$ & $" + str(den) + "$ & " + ref0, end="")
            if latex and s > 3:
                print("\\\\\n\\hline\n$T(" + str(s) + ",2)$ & $2$ & $" + str(num) + "$ & $" + str(den) + "$ & " + ref1, end="")
            if not latex and s == 3:
                print("i(T(3,2)) =", num, "/", den, "\t\t(p,q)=(" + str(p) + "," + str(q) + ") l=2 Reference [0].")
            if not latex and s > 3:
                print("i(T(" + str(s) + ",2)) =", num, "/", den, "\t\t(p,q)=(" + str(p) + "," + str(q) + ") l=2 Reference [1].")
        else:
            bs_condition = pow(1 + 1 / r, s) * (1 - s / (p * (r + 1))) > 1
            if bs_condition:
                l0 = r
            elif not bs_condition and (p > 4 or p == 3 and q >= 2):
                l0 = -1
            else:
                l0 = search(r, q, p)
            if l0 == -1:
                print("i(T(" + str(s) + ","+str(r)+")) = unknown")
            else:
                num = numerator(l0, r, q, p)
                den = denominator(l0, r, q, p)
                gc = gcd(num, den)
                num = num // gc
                den = den // gc
                if bs_condition:
                    cite = ref1
                elif s==5 and r == 3:
                    cite = ref1 + " " + ref5
                elif s==4 and r== 3:
                    cite = ref2
                elif s==5 and r == 4:
                    cite = ref3 + " " + ref4
                elif s == r+1:
                    cite = ref4
                elif p<= 2 or p==3 and q <= 1:
                    cite = ref6
                else:
                    cite = "unknown"
                if not latex:
                    print("i(T(" + str(s) + ","+str(r)+")) =", num, "/", den, "\t\t(p,q)=(" + str(p) + "," + str(q) + ") l=" + str(l0) , cite)
                else:
                    print("\\\\\n\\hline\n$T(" + str(s) + "," + str(r) + ")$ & $" + str(l0) +"$ & $" + str(num) + "$ & $" + str(den) + "$ & " + cite, end="")