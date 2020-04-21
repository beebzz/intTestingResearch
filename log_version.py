from scipy import special
import matplotlib.pyplot as rowPlot
import math
import random
import itertools

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

#Research Attempt #2:
#Now that regular version is complete, we now focus on implementing a potentially
#more efficient approach; adding a logarithmic number of columns then adding a row
#(while there's columns to add that is)

#method assumes that t = 2 and v < 11
def logDiagonalApproach(t,k,v):
    CA = []

    return CA
