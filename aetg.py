from scipy import special
import matplotlib.pyplot as rowPlot
import itertools
import random

#assumes v < 11 and t = 2
def aetgGenerator(t,k,v):
    CA, unseenInteractionCount, unseenInteractions, seenInteractions = [], v**t*(special.binom(k,t)), {}, set()
    test = []
    for location in itertools.combinations(range(k),t):
        location = list(map(str,list(location)))
        location.insert(1,'c'),location.insert(0,'r')
        location = ''.join(location)
        for inter in itertools.product(range(v),repeat=t):
            inter = ''.join(list(map(str,list(inter))))
            unseenInteractions[inter+location] = inter+location

    while len(seenInteractions) < unseenInteractionCount:
        row = [-1]*k
        interToAdd = unseenInteractions.pop(random.choice(list(unseenInteractions.keys())))
        inter  = interToAdd[0:2]
        locationA = int(interToAdd[interToAdd.find('r')+1:interToAdd.find('c')])
        locationB = int(interToAdd[interToAdd.find('c')+1:])
        row[locationA], row[locationB] = int(inter[0]),int(inter[1])
        for pos in range(len(row)):
            if row[pos] != -1:
                continue
            interMap, symbolMap, curMax = {}, {},1
            for sym in range(v):
                interCount = 0
                tempRow = row
                tempRow[pos] = sym
                for i in range(k):
                    for j in range(i+1,k):
                        if tempRow[i] != -1 and tempRow[j] != -1:
                            if ''.join([str(tempRow[i]),str(tempRow[j]),'r',str(i),'c',str(j)]) not in seenInteractions:
                                interCount += 1
                                if sym not in interMap:
                                    interMap[sym] = set()
                                interSet = interMap[sym]
                                interSet.add(''.join([str(tempRow[i]),str(tempRow[j]),'r',str(i),'c',str(j)]))
                                interMap[sym] = interSet
                if interCount >= curMax:
                    curMax = interCount
                    symbolMap[sym] = interCount
            if len(interMap) > 0:
                interToPut = random.choice(list(symbolMap.keys()))
                seenInteractions.update(interMap[interToPut])
                row[pos] = interToPut
            else:
                interToPut = random.choice(range(v))
                row[pos] = interToPut
        CA.append(row)
    return CA

if __name__ == '__main__':
    CALengthsOne,CALengthsTwo,CALengthsThree,CALengthsFour = [],[],[],[]
    for i in range(10):
        CALengthsOne.append(len(aetg(2,7,2)))
        CALengthsTwo.append(len(aetg(2,15,2)))
        CALengthsThree.append(len(aetg(2,15,3)))
        CALengthsFour.append(len(aetg(2,43,5)))
    rowPlot.scatter([1,2,3,4,5,6,7,8,9,10],CALengthsFour)
    rowPlot.xlabel('# of Runs for AETG Algorithm')
    rowPlot.ylabel('N')
    rowPlot.suptitle('t = 2,k = 43,v = 5')
    rowPlot.show()
