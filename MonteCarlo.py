Web VPython 3.2

## ---------------------------------------------------------------------------
##  This is a Monte Carlo simulation of a 2D Ising model using the 
##  Metropolis algorithm as outlined in 'An Introduction to Thermal Physics'
##  by Schroeder.
##
##  In building this program a few things became clear:
##  1. It would be relatively easy to expand this to 3 dimensions.
##  2. Doing so would require a ton of GPU processing power to get to a 
##     substantial number of iterations.    
##  3. Even with the required power, building a grid large enough to yield
##     meaningful results would inhibit the ability to view what's going on
##     inside the grid, thereby hadicaping its usefulness.
##  4. Nicholas Metropolis is the single greatest name ever concocted! There is
##     no way that man wasn't a super vilian with that name.  I'm now furious 
##     that people spent all that time making a movie about boring ol' 
##     Oppenheimer when there was another physicist at Los Alamos with 
##     name Nicholas damn Metropolis!
## ---------------------------------------------------------------------------


import random

class Dipole:
    def __init__(self, x, y, spin, obj):
        self.x = x
        self.y = y
        self.spin = spin
        self.obj = obj
        
        

## Simulation configuration properties ---------------------------------------

N = 100                 # Number of rows & columns of dipoles
T = 2.27                # Temperature
iterationRate = 2000    # Number of iterations per second (estimated)
iterationCap = 1000000  # Max number of iterations to run

dipoles = []
iterationsCounter = 0



## Environment configuration ------------------------------------------------

title = "Currently displaying {:,} dipoles <br><br>"
sceneSize = 700
dipoleSize = 10
scene = canvas(
    background = vector(.5, .5, .5),
    title = title.format(N**2),
    width = sceneSize,
    height = sceneSize,
    )



## Build initial array of N^2 Dipole objects --------------------------------

for j in range(1, N+1):
    for i in range(1, N+1):
        
        spinVal = 0
                    
        r = random.random()
        if r < .5:
            spinVal = 1
        else:
            spinVal = -1
            
        b = box(color=color.white,
            pos=vector((i * dipoleSize)-(N * dipoleSize/2), (j * dipoleSize)-(N * dipoleSize/2) ,0),
            size=vector(dipoleSize,dipoleSize,2))
        d = Dipole(i, j, spinVal, b)

        dipoles.append(d)

## Here be the magic --------------------------------------------------------
   
def calculate_DeltaU(dipole, i, j):
    
    top = 0
    bottom = 0
    right = 0
    left = 0
    
    ## This would be a lot simpler if we didn't have edges, but I don't see
    ## this additional logic slowing things down much.  Nevertheless, here
    ## we're identifying the spin of the selected dipole's neighbors. 
    
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
                
    ## Now that we have the spin of all relative dipoles, we use that to determine
    ## what - if anything - we do to the spin of the selected dipole.
    ## If flipping the spin would reduce the energy, then we flip it.  If not,
    ## we calculate the Boltzmann factor for the system and use that to determine
    ## whether or not to flip the spin.

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
    
    
    
## Every 'iterationRate' times a second, grab a random dipole and calculate 
## its new spin value

while True:
    
    if iterationsCounter <=  iterationCap: 
        rate(iterationRate)
        
        caption = "Iterations: {:,}"
        
        scene.caption = caption.format(iterationsCounter)
        iterationsCounter = iterationsCounter + 1
        
        i = random.randint(1, N)
        j = random.randint(1, N)
        
        for a in range(N**2):
            if dipoles[a].x == i and dipoles[a].y == j:
                calculate_DeltaU(dipoles[a], i, j)
                break
    

