import pandas as pd
import numpy as np
import math
import collections
import statistics
from statistics import mode

class DecisionTree(object):
    def __init__(self,file):
        self.inputFilename = file
        self.outFilename = ""
        self.trainLabels = []
        self.testLabels = []
        self.trainAttr = []
        self.testAttr = []
        self.labelSet = []
        self.splitAttrLow = []
        self.splitLabelsLow = []
        self.splitAttrHigh = []
        self.splitLabelsHigh = []

    def runPipe(self,output,tp):
        self.outFilename = output
        self.formatInputArray(tp)
        splitCriteria = self.findSplitVal(self.trainAttr,self.trainLabels)
        #split the values to make splitAttr and splitLabels
        [self.splitAttrLow, self.splitLabelsLow, self.splitAttrHigh,self.splitLabelsHigh] = self.splitData(splitCriteria,self.trainAttr,self.trainLabels)
        splitCrit2High = []
        splitCrit2Low = []
        #declare all vars
        splitAttr2HighLow = []
        splitLabels2HighLow = []
        splitAttr2HighHigh = []
        splitLabels2HighHigh = []
        splitAttr2LowLow = []
        splitLabels2LowLow = []
        splitAttr2LowHigh = []
        splitLabels2LowHigh = []

        if(not len(set(self.splitLabelsHigh))==1): #Unique set is pure = len is one
            splitCrit2High = self.findSplitVal(self.splitAttrHigh,self.splitLabelsHigh)
            [splitAttr2HighLow, splitLabels2HighLow, splitAttr2HighHigh,splitLabels2HighHigh] = self.splitData(splitCrit2High,self.splitAttrHigh,self.splitLabelsHigh)

        else:
            print("high values pure, no more splitting")
        if(not len(set(self.splitLabelsLow))==1): #Unique set is pure = len is one
            splitCrit2Low = self.findSplitVal(self.splitAttrLow,self.splitLabelsLow)
            [splitAttr2LowLow, splitLabels2LowLow, splitAttr2LowHigh,splitLabels2LowHigh] = self.splitData(splitCrit2Low,self.splitAttrLow,self.splitLabelsLow)
        else:
            print("low values pure, no more splitting")

        try:
            split1HighLabel = mode(self.splitLabelsHigh)
        except:pass
        try:
            split1LowLabel = mode(self.splitLabelsLow)
        except:pass
        try:
            split2HighLowLabel = mode(splitLabels2HighLow)
        except:pass
        try:
            split2HighHighLabel = mode(splitLabels2HighHigh)
        except:pass
        try:
            split2LowLowLabel = mode(splitLabels2LowLow)
        except:pass
        try:
            split2LowHighLabel = mode(splitLabels2LowHigh)
        except:pass
        
        try:
            splitCriteria.append(split1LowLabel)
        except:pass
        try:
            splitCriteria.append(split1HighLabel)
        except: pass
        try:
            splitCrit2Low.append(split2LowLowLabel)
        except: pass
        try:
            splitCrit2Low.append(split2LowHighLabel)
        except: pass
        try:
            splitCrit2High.append(split2HighLowLabel)
        except: pass
        try:
            splitCrit2High.append(split2HighHighLabel)
        except: pass

        print(splitCriteria)
        print(splitCrit2Low)
        print(splitCrit2High)

        classified = self.classifyVals(splitCriteria,splitCrit2Low,splitCrit2High)
        print(classified)

    def splitData(self,splitCrit,dataAttr,dataLabels):
        splitAttr = splitCrit[0]
        splitVal = splitCrit[1]
        splitAttrLow = []
        splitAttrHigh = []
        splitLabLow = []
        splitLabHigh = []
        for i,attr in enumerate(dataAttr):
            if(attr[splitAttr] < splitVal):
                splitAttrLow.append(attr)
                splitLabLow.append(dataLabels[i])  
            else:
                splitAttrHigh.append(attr)
                splitLabHigh.append(dataLabels[i])
        return [splitAttrLow, splitLabLow, splitAttrHigh,splitLabHigh]


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


    def classifyVals(self,splitCriteria,splitCrit2Low,splitCrit2High):
        #split into first two groups
        attr1 = splitCriteria[0]
        splitVal1 = splitCriteria[1]
        lowLabel1 = splitCriteria[2]
        highLabel1 = splitCriteria[3]
        classifiedList = []
        for item in self.testAttr:
            print("Item Tested: "+str(item))
            if(item[attr1] < splitVal1):
                print("split1Low")
                if(any(splitCrit2Low)): #If there's stuff in the list
                    attr2Low = splitCrit2Low[0]
                    splitVal2Low = splitCrit2Low[1]
                    lowLabel2Low = splitCrit2Low[2]
                    highLabel2Low = splitCrit2Low[3]
                    if(item[attr2Low]<splitVal2Low):
                        print("split2LowLow")
                        classifiedList.append(lowLabel2Low)
                    else:
                        print("split2LowHigh")
                        classifiedList.append(highLabel2Low)
                else:
                    print("No split2Low")
                    classifiedList.append(lowLabel1)#If there's no sub-classification, just use that level.
            else:
                print("split1High")
                if(any(splitCrit2High)): #If there's stuff in the list
                    attr2High = splitCrit2High[0]
                    splitVal2High = splitCrit2High[1]
                    lowLabel2High = splitCrit2High[2]
                    highLabel2High = splitCrit2High[3]
                    if(item[attr2High]<splitVal2High):
                        print("split2HighLow")
                        classifiedList.append(lowLabel2High)
                    else:
                        print("split2HighHigh")
                        classifiedList.append(highLabel2High)
                else:
                    print("No split2High")
                    classifiedList.append(highLabel1)#If there's no sub-classification, just use that level.
        return(classifiedList)
        #print("classifiedList")
        #print(classifiedList)                


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
    file = "mp6_DecisionTree\\input24.txt"
    dTree = DecisionTree(file)
    dTree.runPipe("output.txt","code")


if __name__=="__main__":
    main()