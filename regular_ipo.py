from scipy import special
from naive_version import *
from aetg import *
import matplotlib.pyplot as rowPlot
import math
import random
import itertools

"""
Supplemental implementation of regular IPO algorithm to test against Diagonal IPO

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

def ipoGrowth(CA,t,k,v):
    k = k + 1
    unseenInterCount, seenInteractions = int(v**t*(special.binom(k,t))), set()
    unseenInteractions = generateUnseenInters(t,k,v)
    for i in range(len(CA)):
        CA[i].append(-1)
    for row in CA:
        greatestSeen, options, toAdd = -1, {}, -1
        for sym in range(v):
            row[-1] = sym
            if len(interCounter(row,seenInteractions)) >= greatestSeen:
                options[sym] = len(interCounter(row,seenInteractions))
                greatestSeen = len(interCounter(row,seenInteractions))
        if len(options) == 0:
            row[-1] = random.randint(0,v-1)
        else:
            row[-1] = random.choice(list(options.keys()))
            options.pop(row[-1])
        seenInteractions.update(interCounter(row,seenInteractions))
    while len(seenInteractions) < unseenInterCount:
        newRow = [random.randint(0,v-1) for i in range(k)]
        if len(interCounter(newRow,seenInteractions)) >= math.ceil(len(interCounter(newRow,seenInteractions))/(v**t)):
            CA.append(newRow)
            seenInteractions.update(interCounter(newRow,seenInteractions))
    return CA

if __name__ == '__main__':
    for i in range(20):
        testCA = aetgGenerator(2,30,4)
        print("Length of Test CA:",len(testCA))
        print('Diagonal Results:',len(naiveDiagonalGrowth(testCA,2,30,4)))
        print('Original Results:',len(ipoGrowth(testCA,2,30,4)))
