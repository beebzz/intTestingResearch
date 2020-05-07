from scipy import special
import matplotlib.pyplot as rowPlot
import math
import random

#assumes 2 <= t <= 3
def gRandomCAMaker(t,k,v):
    CA = []
    seenInteractions,numOfUnseens = set(),(v**t)*special.binom(k,t)
    unseenCount = 1
    while unseenCount != 0:
        row = [random.randint(0,v-1) for i in range(k)]
        currUnseenCount = 0
        currSeenInteractions = []
        if t == 2:
            for i in range(k):
                for j in range(i+1,k):
                    interaction = ''.join([str(row[i]),str(row[j]),str(i),str(j)])
                    if interaction not in seenInteractions:
                        currUnseenCount += 1
                        currSeenInteractions.append(interaction)
        else:
            for i in range(k):
                for j in range(i+1,k):
                    for m in range(j+1,k):
                        interaction = ''.join([str(row[i]),str(row[j]),str(row[m]),str(i),str(j),str(m)])
                        if interaction not in seenInteractions:
                            currUnseenCount += 1
                            currSeenInteractions.append(interaction)
        numOfUnseens -= currUnseenCount
        unseenCount = currUnseenCount
        if currUnseenCount >= math.ceil(numOfUnseens/(v**t)):
            CA.append(row)
            seenInteractions.update(currSeenInteractions)
    return CA
