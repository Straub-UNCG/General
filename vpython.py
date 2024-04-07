Web VPython 3.2

import random


N = 100
T = 1
iterationRate = 2000

dipoles = []
iterationsCounter = 0

scene.title = f"{N} x {N}  = {N*N} dipoles\n "

L = 1
#scene.range = L
width = 0.5*L/N
depth = 0.2*L/N
spacing = .1

class Dipole:
    def __init__(self, x, y, spin, obj):
        self.x = x
        self.y = y
        self.spin = spin
        self.obj = obj


for j in range(1, N+1):
    for i in range(1, N+1):
        
        spinVal = 0
                    
        r = random.random()
        if r < .5:
            spinVal = 1
        else:
            spinVal = -1
            
        b = box(color=color.white,
            #pos=vector(L*(i/(N-1)-.5),L*(j/(N-1)-.5),3),
            pos=vector((i * width)-(N * width/2), (j * width)-(N * width/2) ,0),
            size=vector(width,width,depth))
        d = Dipole(i, j, spinVal, b)

        dipoles.append(d)

   
def calculate_DeltaU(dipole, i, j):
    
    top = 0
    bottom = 0
    right = 0
    left = 0
    
    for a in range(N**2):
        if i == 1:
            if dipoles[a].x == N and dipoles[a].y == j:
                top = dipoles[a].spin
        else:
            if dipoles[a].x == i-1 and dipoles[a].y == j:
                top = dipoles[a].spin
        
        if i == N:
            if dipoles[a].x == 1 and dipoles[a].y == j:
                bottom = dipoles[a].spin
        else:
            if dipoles[a].x == i+1 and dipoles[a].y == j:
                bottom = dipoles[a].spin

        if j == 1:
            if dipoles[a].x == i and dipoles[a].y == N:
                left = dipoles[a].spin
        else:
            if dipoles[a].x == i and dipoles[a].y == j-1:
                left = dipoles[a].spin
                
        if j == N:
             if dipoles[a].x == i and dipoles[a].y == 1:
                right = dipoles[a].spin
        else:
            if dipoles[a].x == i and dipoles[a].y == j+1:
                right = dipoles[a].spin


    eDiff = 2 * dipole.spin * (top+bottom+left+right)
        
       
    if eDiff <= 0:
        dipole.spin = -dipole.spin
    else:
        if random.random() < exp(-eDiff/T):
            dipole.spin = -dipole.spin
    
    if dipole.spin > 0:
        dipole.obj.color = color.white
    else:
        dipole.obj.color = color.black
    

while True:
    rate(iterationRate)
    
    scene.caption = f"Iterations: {iterationsCounter}"
    iterationsCounter = iterationsCounter + 1
    
    i = random.randint(1, N)
    j = random.randint(1, N)
    
    for a in range(N**2):
        if dipoles[a].x == i and dipoles[a].y == j:
            calculate_DeltaU(dipoles[a], i, j)
            break
    





















