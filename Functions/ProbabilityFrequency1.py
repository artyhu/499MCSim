import numpy as np
import matplotlib.pyplot as plt
# from Forecasting import mcArray, revCOV
import pandas as pd
from scipy.stats import binom

# For data sets without responses (except declined)
rd = pd.read_excel('/Users/arthurhu/Documents/GitHub/499MCSim/database/Book1.xlsx')

graphArr = []
for i in range(0, 24, 1):
    if rd.iloc[i,2] == 'Declined':
        graphArr.append(0)
    elif rd.iloc[i,6] == 0:
        graphArr.append(100)
    elif rd.iloc[i,6] == 1:
            graphArr.append(60)
    elif rd.iloc[i,6] == 2:
            graphArr.append(20)
    elif rd.iloc[i,6] == 3:
            graphArr.append(5)
    else:  
        break

# print(graphArr)




x = [0, 5, 20, 60, 100]
y=[]
y.append(graphArr.count(0))
y.append(graphArr.count(5))
y.append(graphArr.count(20))
y.append(graphArr.count(60))
y.append(graphArr.count(100))

print(y)


# doesnt use accepted but uses declined
plt.rcParams["figure.figsize"] = [10, 7.50]
plt.rcParams["figure.autolayout"] = True
plt.title("Bar graph")
plt.bar( x , y)
plt.xticks(x)
plt.yticks(y)
plt.xlabel('Probability of getting funded (%)')
plt.ylabel('Frequency of Proposals')
plt.show()