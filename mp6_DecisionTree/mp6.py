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
        [attrKeys, splitCand] = self.findSplitVal()
        print(attrKeys)
        print(splitCand)

    def findSplitVal(self):
        all_keys = list(set().union(*(d.keys() for d in self.trainAttr)))
        splitCandidates = [] #will align with all_keys to show
        for k in all_keys:
            #Find all the values of that attribute
            attrVals = [d[k] for d in self.trainAttr if k in d]
            splitCand = self.findSplitCandidates(attrVals)
            splitCandidates.append(splitCand)
        return [all_keys, splitCandidates]

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

    
    def calcInfoGain(self):
        pass

    
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