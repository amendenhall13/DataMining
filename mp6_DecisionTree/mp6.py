import pandas as pd
import numpy as np
import math
import collections

class DecisionTree(object):
    def __init__(self,file):
        self.inputFilename = file
        self.outFilename = ""
        self.trainLabels = []
        self.testLabels = []
        self.trainAttr = []
        self.testAttr = []
        self.labelSet = []
        self.splitAttr = []
        self.splitLabels = []

    def runPipe(self,output,tp):
        self.outFilename = output
        self.formatInputArray(tp)
        splitCriteria = [self.findSplitVal(self.trainAttr,self.trainLabels)]
        #split the values to make splitAttr and splitLabels
        if(not self.isPure(splitCriteria)):
            pass#splitCriteria.append(self.findSplitVal(self.splitAttr,self.splitLabels))
        else:
            splitCriteria.append([-1,-1])
        classified = self.classifyVals(splitCriteria)

    def isPure(self,splitCriteria1):
        pass

    def findSplitVal(self,dataArr,dataLabels):
        all_keys = list(set().union(*(d.keys() for d in dataArr)))
        splitCandidates = [] #will align with all_keys to show
        for k in all_keys:
            #Find all the values of that attribute
            attrVals = [d[k] for d in dataArr if k in d]
            splitCand = self.findSplitCandidates(attrVals)
            splitCandidates.append(splitCand)
        #Calculate information gain for each candidate
        infoGain = []
        infoGainAttr = []
        infoGainCand = []
        infoCount = 0
        self.infoLabel = self.calcInfoLabel(dataLabels)
        for i,key in enumerate(all_keys):
            for j,cand in enumerate(splitCandidates[i]):
                infoGainAttr.append(key)
                infoGainCand.append(cand)
                infoGain.append(self.calcInfoGain(key,cand,dataArr,dataLabels))
        print(infoGain)
        maxGain = max(infoGain)
        maxGainIndex = infoGain.index(maxGain)
        
        #Find index of max info gain
        return [infoGainAttr[maxGainIndex],infoGainCand[maxGainIndex]]

    def findSplitCandidates(self,arr):
        '''Given an array, finds all of the split candidates from it'''
        setArr = list(set(arr))
        itemPrev = setArr[0]
        candList = []
        for i in range(1,len(setArr)):
            item = setArr[i]
            cand = (float(item)+float(itemPrev))/2.0
            candList.append(cand)
            itemPrev = item
        return candList
 
    def calcInfoGain(self,key,cand,attrDict,labList):
        #print("key"+str(key)+" cand "+str(cand))
        infoSplit = 0
        attrValList = []
        for item in attrDict:
            attrValList.append(item[key])
        
        #Generate counts for confusion matrix
        labelsList = list(set(labList))
        self.labelSet = labelsList
        counts = [ [0]*2 for _ in range(len(labelsList))]
        totalSum = 0
        for i,label in enumerate(labList):
            totalSum +=1
            labelRow = labelsList.index(label)
            attr = attrValList[i]
            if(attr < cand): #Below candidate threshold value
                counts[labelRow][0] += 1 #Add a count to the first in the list
            if(attr > cand):
                counts[labelRow][1] += 1
        
        #Calculate totals for division
        lowSum = 0
        highSum = 0
        for labelRow in counts:
            lowSum += labelRow[0]
            highSum += labelRow[1]
        #Calculate info gain for less than threshold
        infoDLow = 0
        infoDHigh = 0
        for labelRow in counts:
            if(labelRow[0] !=0):
                infoDLow -= labelRow[0]/lowSum*math.log(labelRow[0]/lowSum,2)
            if(labelRow[1] !=0):
                infoDHigh -= labelRow[1]/highSum*math.log(labelRow[1]/highSum,2)
        infoSplit = lowSum/totalSum*infoDLow + highSum/totalSum*infoDHigh
        gain = self.infoLabel-infoSplit
        return gain

    def calcInfoLabel(self,dataLabels):
        counts = list(dict(collections.Counter(dataLabels)).values())
        totalCount = sum(counts)
        infoGainLabel = 0
        for val in counts:
            infoGainLabel -= val/totalCount*math.log(val/totalCount,2)
        return infoGainLabel


    def classifyVals(self,splitCriteria):
        print(splitCriteria)
        firstCrit = splitCriteria[0]
        attr1 = firstCrit[0]
        val1 = firstCrit[1]
        secCrit = splitCriteria[1]
        attr2 = secCrit[0]
        val2 = secCrit[1]
        #split into first two groups
        classifiedList = []
        for item in self.testAttr:
            if(item[attr1] < val1):
                classifiedList.append(self.labelSet[0])
            else:
                classifiedList.append(self.labelSet[1])
        print(classifiedList)                


    def formatInputArray(self,tp):
        if(tp=="code"): #Read input with pandas from text file for testing.
            nrows_ = 100
            df = pd.read_csv(self.inputFilename,header=None,sep="\n")#,nrows = nrows_)
            df = df[0].str.split(" ",expand=True)
            #print(df)
            trainLabels = []
            trainAttr = []
            testLabels = []
            testAttr = []
            for i,row in df.iterrows():
                rowAttr = {}
                rowLabel = -2
                for j,item in row.items():
                    #print(item)
                    if j == 0:
                        rowLabel = int(float(item))
                    else:
                        #put attr stuff into a dict
                        valList = item.split(":")
                        #print(valList)
                        attrNum = int(float(valList[0].strip(''))) #split attr name and value
                        attrVal = float(valList[1].strip(''))
                        rowAttr[attrNum] = attrVal
                    
                    #Append row to new data structures based on test or train
                    #print(type(rowLabel))
                if(rowLabel == -1):
                    #+print("hi")
                    testLabels.append(rowLabel)
                    testAttr.append(rowAttr)
                else:
                    trainLabels.append(rowLabel)
                    trainAttr.append(rowAttr)            
        if(tp=="hack"):
            '''Not implemented yet'''
            inArray = []
            stop = False
            while not stop:
                try:
                    temp = input()
                    separate = temp.split()
                    separate[0] = float(separate[0])
                    separate[1] = float(separate[1])
                    inArray.append(separate)
                except:
                    stop = True
            self.inArray = inArray
        
        self.testLabels = testLabels
        self.testAttr = testAttr
        self.trainLabels = trainLabels
        self.trainAttr = trainAttr
        


def main():
    file = "mp6_DecisionTree\\sample0.txt"
    dTree = DecisionTree(file)
    dTree.runPipe("output.txt","code")


if __name__=="__main__":
    main()