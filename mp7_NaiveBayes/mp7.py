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

        #[1,2,3,4,6,7] -- all possible class labels, sorted
        self.classList = [1,2,3,4,5,6,7] #done in formatInputArray
        #[3,3,3,3,3] -- counts for each class matched to classList order.
        self.countByClass = [] #len(#classes), done in calcpOfc
        
        
        self.pOfc = [] #len(#classes)
        self.pOfXUnderC = [] #len(#classes)

    def runPipe(self,output,tp):
        [trainVals,trainLabels,testVals] = self.formatInputArray(tp)
        self.pOfc = self.calcpOfc(trainLabels)
        '''for testVal in unknownList:
            self.pOfXUnderC = self.calcpOfxUnderc(testVal)
            totalProbList = [a*b for a,b in zip(self.pOfc,self.pOfXUnderC)] #element by element matrix multiplication
            maxProb = max(totalProbList)
            #Linked classList/probList to find index and therefore find class.
            cls = self.classList[totalProbList.index(maxProb)] 
            print(cls)'''



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



            

        

    def calcpOfxUnderc(self,testVal):
        '''Return array of len(#classes) with L-corrected probabilty of x under c'''
        pass


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
        return [0,1]
        '''return [knownList,unknownList]'''

def main():
    file = "mp7_NaiveBayes\\sample0.txt"
    dTree = NaiveBayes(file)
    dTree.runPipe("output.txt","code")


if __name__=="__main__":
    main()