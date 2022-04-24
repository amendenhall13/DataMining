import pandas as pd
import numpy as np
import math
import collections
import statistics
from statistics import mode

class NaiveBayes(object):
    def __init__(self,file):
        self.inputFilename = file
        self.animalName = [] #list of animal names [[trainList],[testList]], in formatInputData

        #["hair","feathers","fins"] etc
        self.attrList = [] #len(#attr), all attr names, done in formatInputArray
        #[2,2,2,2] -- 2 for booleans, 6 for leg
        self.optionsByVar = [2,2,2,2,2,2,2,2,2,2,2,2,6,2,2,2] #How many options does each var have? len(#attr)
        self.optionsList = [] #Made in makeConfusionMatrix

        #[1,2,3,4,6,7] -- all possible class labels, sorted
        self.classList = [1,2,3,4,5,6,7] #done in formatInputArray
        #[3,3,3,3,3] -- counts for each class matched to classList order.
        self.countByClass = [] #len(#classes), done in calcpOfc
        #[class1->[ctAttr1,ctAttr2],
        # class2->[ctAttr1,ctAttr2]]...
        self.confusionMatrix = []
        
        self.pOfc = [] #len(#classes)
        self.pOfXUnderC = [] #len(#classes)

    def runPipe(self,output,tp):
        [trainVals,trainLabels,testVals] = self.formatInputArray(tp)
        self.pOfc = self.calcpOfc(trainLabels)
        self.confusionMatrix = self.makeConfusionMatrix(trainVals,trainLabels)
        for test in testVals:
            self.pOfXUnderC = self.calcpOfxUnderc(test)
            totalProbList = [a*b for a,b in zip(self.pOfc,self.pOfXUnderC)] #element by element matrix multiplication
            maxProb = max(totalProbList)
            #Linked classList/probList to find index and therefore find class.
            cls = self.classList[totalProbList.index(maxProb)] 
            print(cls)

    def calcpOfxUnderc(self,testVal):
        '''Return array of len(#classes) with L-corrected probabilty of x under c'''
        probMatrix = []
        for i,cls in enumerate(self.classList):
            probForOneClass = []
            for j,attr in enumerate(self.attrList):
                confRow = i #ClassList is the row index for the confusion matrix as well as the probabilty matrix
                #testVal linked to attrList to find confCol
                confCol = self.optionsList.index(str(attr)+str(int(testVal[j])))
                countpXC = self.confusionMatrix[confRow][confCol]
                countC = self.countByClass[i] #Linked to classList
                numFeatures = self.optionsByVar[j] #Linked to attrList
                prob = (countpXC+0.1)/(countC+0.1*numFeatures)
                probForOneClass.append(prob)
            probMatrix.append(probForOneClass)
        pXunderC = []
        for row in probMatrix:
            colProduct = 1
            for col in row:
                colProduct *= col
            pXunderC.append(colProduct)
        return pXunderC
            
            
                

    def makeConfusionMatrix(self,trainVals,trainLabels):
        '''Create the confusion matrix of the counts first so don't have to repeatedly loop through'''
        #Make the optionsList by filling in 0/1 for all values and then changing the non-boolean one
        for i,attr in enumerate(self.attrList):
            for i in range(self.optionsByVar[i]): #loop through the number of times the var is, i.e. 1-6
                self.optionsList.append(attr+str(i))
        #replace legs numbers with appropriate one
        self.optionsList = list(map(lambda x: x.replace("legs1", 'legs6'), self.optionsList))
        self.optionsList = list(map(lambda x: x.replace("legs3", 'legs8'), self.optionsList))
        
        #Make confusion matrix of 0s
        confusionMatrix = [ [0]*len(self.optionsList) for _ in range(len(self.classList)) ]
        #Go through training values/labels and add onto the appropriate matrix locations
        for i,dataLabel in enumerate(trainLabels):
            confRow = self.classList.index(dataLabel) #The confusion matrix row index is looked up from the classList
            #Create col lookup in confMatrix by adding the attrList lookup to the value at that index in the attrList
            for j,attrVal in enumerate(trainVals[i]):
                attrLabel = self.attrList[j]
                confColString = attrLabel + str(int(attrVal))
                confCol = self.optionsList.index(confColString)
                confusionMatrix[confRow][confCol] += 1
        return confusionMatrix

    def calcpOfc(self,trainLabels):
        '''Return an array of len(#classes) with Laplacian-corrected probability of each.
            Also updates self.countByClass'''
        #Create a running total and individual class totals       
        totalSum = 0
        for cls in self.classList:
            numInstances = trainLabels.count(cls)
            self.countByClass.append(numInstances)
            totalSum += numInstances
        
        pOfc = []
        for i,cls in enumerate(self.classList):
            numClassesPresent = len(set(self.classList))
            prob = (self.countByClass[i]+0.1)/(totalSum+0.1*numClassesPresent)
            pOfc.append(prob)
        return pOfc

    def formatInputArray(self,tp):
        if(tp=="code"): #Read input with pandas from text file for testing.
            df = pd.read_csv(self.inputFilename,header=None,sep="\n")
            df = df[0].str.split(",",expand=True)
            listVals = df.values.tolist()

            self.attrList = listVals[0]
            labelIndex = self.attrList.index("class_type")
            nameIndex = self.attrList.index("animal_name")
            self.attrList = [x for i,x in enumerate(listVals[0]) if (i!=labelIndex and i!=nameIndex)]
            listVals = listVals[1:]
            trainLabels = []
            trainVals = []
            trainAnimalName = []
            testLabels = []
            testVals = []
            testAnimalName = []
            #split values into 6 lists
            for val in listVals:
                if(val[labelIndex] != '-1'):
                    trainLabels.append(val[labelIndex])
                    trainAnimalName.append(val[nameIndex])
                    trainVals.append([x for i,x in enumerate(val) if (i!=labelIndex and i!=nameIndex)]) #add all other values to trainVals
                else:
                    testLabels.append(val[labelIndex])
                    testAnimalName.append(val[nameIndex])
                    testVals.append([x for i,x in enumerate(val) if (i!=labelIndex and i!=nameIndex)]) #add all other values to testVals
            #cast appropriate lists as floats
            for i,row in enumerate(trainVals):
                for j,col in enumerate(row):
                    trainVals[i][j] = float(trainVals[i][j])
            for i,row in enumerate(testVals):
                for j,col in enumerate(row):
                    testVals[i][j] = float(testVals[i][j])
            for i,row in enumerate(trainLabels):
                    trainLabels[i] = float(trainLabels[i])
            for i,row in enumerate(testLabels):
                    testLabels[i] = float(testLabels[i])

            #self.classList = list(set(trainLabels)) # Class list is static, even if train set doesn't have it
            #self.classList.sort()
            self.animalName = [trainAnimalName,testAnimalName] #Probably don't need it, stored anyway.
            return [trainVals,trainLabels,testVals]
           
        '''if(tp=="hack"):
            pass'''


def main():
    file = "mp7_NaiveBayes\\input5.txt"
    dTree = NaiveBayes(file)
    dTree.runPipe("output.txt","code")


if __name__=="__main__":
    main()