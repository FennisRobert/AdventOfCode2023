from sympy import *

Nterms = 4

Sx, Sy, Sz, Vx, Vy, Vz = symbols('Sx Sy Sz Vx Vy Vz')
t = symbols('t')
deqs = []
for i in range(1,Nterms+1):
    
    six, siy, siz, vix, viy, viz = symbols(f's{i}x s{i}y s{i}z v{i}x v{i}y v{i}z')
    
    dist = sqrt((six-Sx + t*(vix-Vx))**2 + (siy-Sy + t*(viy-Vy))**2 + (siz-Sz + t*(viz-Vz))**2 )
    
    dddt = diff(dist, t)
    t1 = solve(dddt*dist, t)[0]
    d1 = dist.subs(t,t1)
    deqs.append(d1**2)

Dtot = sum(deqs)

Ddsx = Dtot.diff(Sx)
Ddsy = Dtot.diff(Sy)
Ddsz = Dtot.diff(Sz)
Ddvx = Dtot.diff(Vx)
Ddvy = Dtot.diff(Vy)
Ddvz = Dtot.diff(Vz)

print(solve(Ddsx, Sx))