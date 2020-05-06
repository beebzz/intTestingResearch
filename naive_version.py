from scipy import special
from regular_ipo import *
import matplotlib.pyplot as rowPlot
import math
import random
import itertools

"""
 Research Attempt #1:
 approach was to pick random symbol from v, then constructively add one column & one row at a time
 to CA via adding one value to right of rightmost topmost value, and one value underneath leftmost bottommost
 value then find best value to add for every don't care position (or random if you can't add any new interactions)

 Result:
 The algorithm functions for any value of t, k and v where t < 2 and v < 11. However, we had
 to alter our original approach by forcing random interactions in newly added rows instead of
 single random symbols
"""

"""Helper"""
def interCounter(row, seenInteractions):
  CA = []
  newInters = set()
  for i in range(len(row)):
      for j in range(i+1,len(row)):
          if row[i] != -1 and row[j] != -1:
              interaction = ''.join([str(row[i]),str(row[j]),'r',str(i),'c',str(j)]);
              if interaction not in seenInteractions:
                  newInters.add(interaction)
  return newInters

"""Helper"""
def generateUnseenInters(t,k,v):
    unseenInteractions = {}
    for location in itertools.combinations(range(k),t):
        location = list(map(str,list(location)))
        location.insert(1,'c'),location.insert(0,'r')
        location = ''.join(location)
        for inter in itertools.product(range(v),repeat=t):
            inter = ''.join(list(map(str,list(inter))))
            unseenInteractions[inter+location] = inter+location
    return unseenInteractions

"""Generation Algorithm (method assumes that t = 2 and v < 11)"""
def naiveDiagonalApproach(t,k,v):
    CA = []
    random_sym, unseenInterCount, seenInteractions = random.randint(0,v-1), int(v**t*(special.binom(k,t))), set()
    unseenInteractions = generateUnseenInters(t,k,v)
    initRow = [-1]*(k-1)
    initRow.insert(0,random_sym)
    CA.append(initRow)
    while len(seenInteractions) < unseenInterCount:
        benchmark = -1
        if -1 in CA[0]:
            for i in range(len(CA[0])):
                if CA[0][i] == -1:
                    CA[0][i] = random.randint(0,v-1)
                    benchmark = i+1
                    break
        if benchmark == -1:
            benchmark = len(CA[0])
        newRow = [-1]*(k)
        interToAdd = unseenInteractions.pop(random.choice(list(unseenInteractions.keys())))
        inter  = interToAdd[0:2]
        locationA = int(interToAdd[interToAdd.find('r')+1:interToAdd.find('c')])
        locationB = int(interToAdd[interToAdd.find('c')+1:])
        newRow[locationA], newRow[locationB] = int(inter[0]),int(inter[1])
        CA.append(newRow)
        for row in CA:
            for i in range(benchmark):
                if row[i] == -1:
                    greatestSeen, options, toAdd = -1, {}, -1
                    for sym in range(v):
                        row[i] = sym
                        if len(interCounter(row,seenInteractions)) >= greatestSeen:
                            options[sym] = len(interCounter(row,seenInteractions))
                            greatestSeen = len(interCounter(row,seenInteractions))
                    if len(options) == 0:
                        row[i] = random.randint(0,v-1)
                    else:
                        row[i] = random.choice(list(options.keys()))
                        options.pop(row[i])
                    seenInteractions.update(interCounter(row,seenInteractions))
    return CA

"""Growth Algorithm (method assumes that t = 2 and v < 11)"""
def naiveDiagonalGrowth(CA,t,k,v):
    k = k+1
    unseenInterCount, seenInteractions = int(v**t*(special.binom(k,t))), set()
    unseenInteractions = generateUnseenInters(t,k,v)
    for row in CA:
        seenInteractions.update(interCounter(row,seenInteractions))
    CA[0].append(random.randint(0,v-1))
    for i in range(1,len(CA)):
        CA[i].append(-1)
    while len(seenInteractions) < unseenInterCount:
        newRow = [-1]*(k)
        interToAdd = unseenInteractions.pop(random.choice(list(unseenInteractions.keys())))
        inter  = interToAdd[0:2]
        locationA = int(interToAdd[interToAdd.find('r')+1:interToAdd.find('c')])
        locationB = int(interToAdd[interToAdd.find('c')+1:])
        newRow[locationA], newRow[locationB] = int(inter[0]),int(inter[1])
        CA.append(newRow)
        for row in CA:
            for i in range(len(row)):
                if row[i] == -1:
                    greatestSeen, options, toAdd = -1, {}, -1
                    for sym in range(v):
                        row[i] = sym
                        if len(interCounter(row,seenInteractions)) >= greatestSeen:
                            options[sym] = len(interCounter(row,seenInteractions))
                            greatestSeen = len(interCounter(row,seenInteractions))
                    if len(options) == 0:
                        row[i] = random.randint(0,v-1)
                    else:
                        row[i] = random.choice(list(options.keys()))
                        options.pop(row[i])
                    seenInteractions.update(interCounter(row,seenInteractions))
    return CA

"""Testing and Figure Generation"""
if __name__ == '__main__':
    CALengthsOne, CALengthsTwo, CALengthsThree = [],[],[]
    for i in range(10):
        CALengthsOne.append(len(naiveDiagonalApproach(2,15,2)))
        CALengthsTwo.append(len(naiveDiagonalApproach(2,30,4)))
        CALengthsThree.append(len(naiveDiagonalApproach(2,43,5)))
    rowPlot.scatter([1,2,3,4,5,6,7,8,9,10],CALengthsOne)
    rowPlot.xlabel('# of Runs for Diagonal IPO Generation Algo.')
    rowPlot.ylabel('N')
    rowPlot.suptitle('t = 2,k = 15,v = 2')
    rowPlot.show()
    rowPlot.scatter([1,2,3,4,5,6,7,8,9,10],CALengthsTwo)
    rowPlot.xlabel('# of Runs for Diagonal IPO Generation Algo.')
    rowPlot.ylabel('N')
    rowPlot.suptitle('t = 2,k = 30,v = 4')
    rowPlot.show()
    rowPlot.scatter([1,2,3,4,5,6,7,8,9,10],CALengthsThree)
    rowPlot.xlabel('# of Runs for Diagonal IPO Generation Algo.')
    rowPlot.ylabel('N')
    rowPlot.suptitle('t = 2,k = 43,v = 5')
    rowPlot.show()
