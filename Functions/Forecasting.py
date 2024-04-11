import random
import numpy as np
from scipy.stats import bernoulli
from scipy.stats import binom
import mysql.connector
from mysql.connector import connect, Error
import pandas as pd
import statistics
import math


def pert(a, b, c, size=1, lamb=4):
    r = c - a
    alpha = 1 + lamb * (b - a) / r
    beta = 1 + lamb * (c - b) / r
    return float(a + np.random.beta(alpha, beta, size=size) * r)

rd = pd.read_excel('/Users/arthurhu/Documents/GitHub/499MCSim/Data/Book1.xlsx')
# link for the binom().rvs https://discovery.cs.illinois.edu/learn/Polling-Confidence-Intervals-and-Hypothesis-Testing/Python-Functions-for-Random-Distributions/#:~:text=pmf()%20and%20.,a%20fixed%20probability%20of%20occurring.


def MonteCarloSim():
    totRev=0
    a = (binom(p=.6, n=1).rvs(10000)) # 10000 iterations of each probability
    aCount = np.bincount(a)         # then takes what occurs more (0 or 1)
    b = (binom(p=0.2, n=1).rvs(10000))
    bCount = np.bincount(b)
    c = (binom(p=0.05, n=1).rvs(10000))
    cCount = np.bincount(c)
    # this model really doesnt account for LOC 3 well. in the excel file there are two MG that total to 45k that in this model have a 5% chance of occuring each
    for i in range(0, 24, 1):
        if rd.iloc[i,2] == 'Declined':  # Suggestion from Dr. Meger implelemented - good way to reduce unneccessary calculations
            continue
        elif rd.iloc[i,6] == 0:
            # if LOC = 0 that means the donation is a lock and the DA is added to the totRev - the model just adds DA, but some are variable- should there be another factor in this?
            # iloc (i,5) 5 is the money recieved, should be changed to the ask amt value
            totRev += (rd.iloc[i, 5])
        elif rd.iloc[i,6] == 1:
            # print("a", np.argmax(aCount)) --- 1 goes through, 0 doesnt
            # print("LOC1", i)
            if (np.argmax(aCount)) == 1: 
                totRev += ((rd.iloc[i, 3]) * pert(0.985, 1, 1.015))
        elif rd.iloc[i,6] == 2:
            # print("b", np.argmax(bCount))
            # print("LOC2", i)
            if (np.argmax(bCount)) == 1:
                totRev += ((rd.iloc[i, 3]) * pert(0.985, 1, 1.015))
        elif rd.iloc[i,6] == 3:
            # print("c", np.argmax(cCount))
            # print("LOC3", i)
            if (np.argmax(cCount)) == 1:
                totRev += ((rd.iloc[i, 3]) * pert(0.985, 1, 1.015))
        else:  
            break
    return totRev


# new function to run MonteCarloSim 1xxxx times and stores in array.
# will be used for graphing as well as coeff of variation
def mcArray():
    revArr = []
    for k in range(0, 1000, 1): # change to 10,000 later on(atm just takes too long to execute) also change the MEAN equation 
        mc = (MonteCarloSim())
        revArr.append(mc)
    return revArr

# print(mcArray())  

# original mcArray below (not defined as a func)
# arr=[]
# for k in range(0, 1000, 1):
#     mc = MonteCarloSim()
#     arr.append(mc)
# print(arr) 
mean = ((sum(mcArray()))/1000) 

def revCOV():
    # print(mean)
    # print(statistics.stdev(mcVariance(), mean))
    return (((statistics.pstdev(mcArray(), mean))/mean)*100)

def bigMCArray():
    newArr = []
    for k in range(0,10, 1):
        y = ((sum(mcArray()))/1000)
        newArr.append(y)
        print(y)
    return newArr

bigMean = ((sum(bigMCArray()))/10)

# margin of error / use a different calculation- CI is too narrow to be true 
MOE = (1.645)*((statistics.pstdev(mcArray(), mean)/math.sqrt(1000)))

MOE2 = (1/math.sqrt(1000)) * mean # same link for MOE2 & MOE3 https://bookdown.org/kevin_davisross/probsim-book/moe.html#

MOE3 = (1.645) * ((math.sqrt(.5*(1-.5)))/(math.sqrt(1000))) * mean # seems the most accurate, uses arbitrary p value of .5 as this is conservative and p=unknown



# print(MOE, MOE2, MOE3, "\n")
print("Actual Total Revenue:", "$2,747,152.31","\n")

print("Total revenue with 1 Simulation:","$", MonteCarloSim(), "\n")
print("Total Revenue Mean with 1000 Simulations:", "$", (mean), "\n")

print("Total Revenue Mean with 10 x 1000 Simulations:", "$", (bigMean), "\n")


print("Coefficient of Variability:", revCOV(), "%\n")
# print("Original-Simulated 90% CI MG Revenue:", "$", (mean - MOE), "to", "$", (mean + MOE), "\n")
# print("2nd-Simulated 90% CI MG Revenue:", "$", (mean - MOE2), "to", "$", (mean + MOE2), "\n")
print("Simulated 90% CI MG Revenue:", "$", (mean - MOE3), "to", "$", (mean + MOE3), "\n")


