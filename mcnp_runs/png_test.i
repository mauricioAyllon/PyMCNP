Embedded source simulation of PNG
c
c ===============================================================
c                        cell definitions
c ===============================================================
c cell
1       0  -8    imp:n=1
2       0   8    imp:n=0 $ outside world
c

c ===============================================================
c                       surface definitions
c ===============================================================
c neutron surface for tally
c
8 so  1     $ outside world
c         ***** Anything else? *****
c
c ===============================================================

c          *****physics and tracking*****
c turn on elastic recoil and NCIA
c phys:n 50000 5j 4 100
c enable photonuclear physics
c phys:p 100 2j -1
c cut:h,t,d,s,a,# j 1e-8
cut:n 100000000 j 0 0
mode n
c
c
c ===============================================================
c          *****material compositions*****
c
m0 nlib=80c
c Aluminum is 7.874 g/cm3
m13      13027 1
c
c Source definition 
c
c burst=10 us
c period=35 us
c burst packets=32
c capture gate=380 us
c sigma packets=3
sdef par=n erg=14 TME=D1<D2
# SI1 SP1
0  0 
10e2  1
35e2 0
45e2  1
70e2 0
80e2  1
105e2 0
115e2  1
140e2 0
150e2  1
175e2 0
185e2  1
210e2 0
220e2  1
245e2 0
255e2  1
280e2 0
290e2  1
315e2 0
325e2  1
350e2 0
360e2  1
385e2 0
395e2  1
420e2 0
430e2  1
455e2 0
465e2  1
490e2 0
500e2  1
525e2 0
535e2  1
560e2 0
570e2  1
595e2 0
605e2  1
630e2 0
640e2  1
665e2 0
675e2  1
700e2 0
710e2  1
735e2 0
745e2  1
770e2 0
780e2  1
805e2 0
815e2  1
840e2 0
850e2  1
875e2 0
885e2  1
910e2 0
920e2  1
945e2 0
955e2  1
980e2 0
990e2  1
1015e2 0
1025e2  1
1050e2 0
1060e2  1
1085e2 0
1095e2 1
1500e2 0
# SI2 SP2 
0 0
4500e2 1 
c ===============================================================
c
t0 0 4499i 4500e2
f2:n   8
fq2  t  f
c
c ===============================================================
nps    100000
