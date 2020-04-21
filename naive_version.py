from scipy import special
import matplotlib.pyplot as rowPlot
import math
import random
import itertools

# Research Attempt #1:
# approach was to pick random symbol from v, then constructively add one column & one row at a time
# to CA via adding one value to right of rightmost topmost value, and one value underneath leftmost bottommost
# value then find best value to add for every don't care position (or random if you can't add any new interactions)

# Result:
# The algorithm functions for any value of t, k and v where t < 2 and v < 11. However, we had
# to alter our original approach by forcing random interactions in newly added rows instead of
# single random symbols

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

#method assumes that t = 2 and v < 11
def naiveDiagonalApproach(t,k,v):
    CA = []
    # pick random symbol to start the covering array with
    random_sym, unseenInterCount, seenInteractions = random.randint(0,v-1), int(v**t*(special.binom(k,t))), set()
    unseenInteractions = generateUnseenInters(t,k,v)
    initRow = [-1]*(k-1)
    initRow.insert(0,random_sym)
    CA.append(initRow)
    # while there's unseen interactions:
    while len(seenInteractions) < unseenInterCount:
        # add random symbol to right of upperrightmost symbol
        benchmark = -1
        if CA[0][-1] == -1:
            for i in range(len(CA[0])):
                if CA[0][i] == -1:
                    CA[0][i] = random.randint(0,v-1)
                    benchmark = i+1
                    break
        if benchmark == -1:
            benchmark = len(row)
        newRow = [-1]*(k)
        #change to force random interaction instead of random symbol
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

def naiveDiagonalGrowth(CA,t,k,v):
    #incease k by 1
    k = k+1
    #print(t,k,v)
    unseenInterCount, seenInteractions = int(v**t*(special.binom(k,t))), set()
    unseenInteractions = generateUnseenInters(t,k,v)
    for row in CA:
        seenInteractions.update(interCounter(row,seenInteractions))
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
        row[-1] = options.pop(random.choice(list(options.keys())))
        seenInteractions.update(interCounter(row,seenInteractions))
    while len(seenInteractions) < unseenInterCount:
        newRow = [-1]*(k)
        #change to force random interaction instead of random symbol
        interToAdd = unseenInteractions.pop(random.choice(list(unseenInteractions.keys())))
        inter  = interToAdd[0:2]
        locationA = int(interToAdd[interToAdd.find('r')+1:interToAdd.find('c')])
        locationB = int(interToAdd[interToAdd.find('c')+1:])
        newRow[locationA], newRow[locationB] = int(inter[0]),int(inter[1])
        CA.append(newRow)
        # for every don't care(-1's), either pick symbol that
        # maximizes coverage, or pick random if coverage can't be maximized
        for i in range(len(CA[-1])):
            greatestSeen, options, toAdd = -1, {}, -1
            for sym in range(v):
                CA[-1][i] = sym
                if len(interCounter(CA[-1],seenInteractions)) >= greatestSeen:
                    options[sym] = len(interCounter(CA[-1],seenInteractions))
                    greatestSeen = len(interCounter(CA[-1],seenInteractions))
            if len(options) == 0:
                CA[-1][i] = random.randint(0,v-1)
            CA[-1][i] = options.pop(random.choice(list(options.keys())))
            seenInteractions.update(interCounter(CA[-1],seenInteractions))

    return CA

if __name__ == '__main__':
    CALengthsOne, CALengthsTwo = [],[]
    for i in range(5):
        result = naiveDiagonalApproach(2,14,2)
        print(len(result),len(naiveDiagonalApproach(2,15,2)))
        CALengthsOne.append(len(result))
        print(len(naiveDiagonalGrowth(result,2,14,2)))
        #CALengthsTwo.append(len(naiveDiagonalGrowth(result,2,15,2)))
    #rowPlot.scatter([1,2,3,4,5],CALengthsOne)
    #rowPlot.xlabel('# of Runs for Diagonal IPO Generation Algo.')
    #rowPlot.ylabel('N')
    #rowPlot.suptitle('t = 2,k = 15,v = 2')
    #rowPlot.show()
    #rowPlot.scatter([1,2,3,4,5],CALengthsTwo)
    #rowPlot.xlabel('# of Runs for Diagonal IPO Growth Algo.')
    #rowPlot.ylabel('N')
    #rowPlot.suptitle('t = 2,k = 16,v = 2')
    #rowPlot.show()
