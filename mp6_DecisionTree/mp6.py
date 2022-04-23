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

    def runPipe(self,output,tp):
        self.outFilename = output
        self.formatInputArray(tp)
        val = self.findSplitVal()
        

    def findSplitVal(self):
        all_keys = list(set().union(*(d.keys() for d in self.trainAttr)))
        splitCandidates = [] #will align with all_keys to show
        for k in all_keys:
            #Find all the values of that attribute
            attrVals = [d[k] for d in self.trainAttr if k in d]
            splitCand = self.findSplitCandidates(attrVals)
            splitCandidates.append(splitCand)
        #Calculate information gain for each candidate
        infoGain = []
        infoGainAttr = []
        infoGainCand = []
        infoCount = 0
        self.infoLabel = self.calcInfoLabel()
        for i,key in enumerate(all_keys):
            for j,cand in enumerate(splitCandidates[i]):
                infoGainAttr.append(key)
                infoGainCand.append(cand)
                infoGain.append(self.calcInfoGain(key,cand))
        #Find index of max info gain
        '''TBD'''

                


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

    
    def calcInfoGain(self,key,cand):
        print("key"+str(key)+" cand "+str(cand))
        infoSplit = 0
        attrValList = []
        for item in self.trainAttr:
            attrValList.append(item[key])
        
        #Generate counts for confusion matrix
        labelsList = list(set(self.trainLabels))
        counts = [ [0]*2 for _ in range(len(labelsList))]
        totalSum = 0
        for i,label in enumerate(self.trainLabels):
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
        print(infoDLow)
        print(infoDHigh)
        print(totalSum)
        
        gain = self.infoLabel-infoSplit
        return gain

    def calcInfoLabel(self):
        counts = list(dict(collections.Counter(self.trainLabels)).values())
        totalCount = sum(counts)
        infoGainLabel = 0
        for val in counts:
            infoGainLabel -= val/totalCount*math.log(val/totalCount,2)
        return infoGainLabel


    def classifyVals(self):
        pass  

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