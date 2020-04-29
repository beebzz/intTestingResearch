from scipy import special
import matplotlib.pyplot as rowPlot
import math
import random
import itertools

"""
 Research Attempt #2:
    Now that regular version is complete, we now focus on implementing a potentially
    more efficient approach; adding a logarithmic number of columns then adding a row
    (while there's columns to add that is)
"""

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


"""Generation Algo (method assumes that t = 2 and v < 11)"""
def logDiagonalApproach(t,k,v):
    CA = []
    # pick random symbol to start the covering array with
    random_sym, unseenInterCount, seenInteractions = random.randint(0,v-1), int(v**t*(special.binom(k,t))), set()
    unseenInteractions = generateUnseenInters(t,k,v)
    initRow = [-1]*(k-1)
    initRow.insert(0,random_sym)
    CA.append(initRow)
    # while there's unseen interactions:
    #print(unseenInterCount)
    while len(seenInteractions) < unseenInterCount:
        # same strategy as naive except add a logarithmic number of columns,
        # instead of one, proportional to the remaining number of unfilled columns
        remColumns, colsToAdd = 0, 1
        benchmark = 0
        for i in range(len(CA[0])):
            if CA[0][i] == -1:
                remColumns += 1
        if remColumns > 0:
            #print("remaining cols",remColumns)
            colsToAdd = math.floor(math.log(remColumns))
            colCount = colsToAdd
            #print('cols to add',colsToAdd)
            j = 0
            while j < len(CA[0]) and colCount > 0:
                if CA[0][j] == -1:
                    CA[0][j] = random.randint(0,v-1)
                    benchmark += 1
                    colCount -= 1
                j += 1
        else:
            benchmark = len(CA[0])
        for j in range(colsToAdd):
            newRow = [-1]*(k)
            for i in range(colsToAdd):
                interToAdd = unseenInteractions.pop(random.choice(list(unseenInteractions.keys())))
                inter  = interToAdd[0:2]
                locationA = int(interToAdd[interToAdd.find('r')+1:interToAdd.find('c')])
                locationB = int(interToAdd[interToAdd.find('c')+1:])
                newRow[locationA], newRow[locationB] = int(inter[0]),int(inter[1])
            CA.append(newRow)
        # for every don't care(-1's), either pick symbol that
        # maximizes coverage, or pick random if coverage can't be maximized
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
                    row[i] = options.pop(random.choice(list(options.keys())))
                    seenInteractions.update(interCounter(row,seenInteractions))
    return CA

def logDiagonalGrowth(CA,t,k,v):
    # add logarithmic # of columns proportional to k (add log(k) columns)
    # then fill in necessary rows
        # if logarithmic # is < 1, just add 1 (i.e. utilize the naive growth approach instead)
    return CA

if __name__ == '__main__':
    print(logDiagonalApproach(2,15,2))
