import pandas as pd
import numpy as np
import math
import collections

class aggCluster:
    def __init__(self,file):
        self.inArray = []
        self.n = 0
        self.outFilename = ""
        self.inputFilename = file
        self.jaccard = 0
        self.nmi = 0

    def runPipe(self,output,tp):
        self.outFilename = output
        self.formatInputArray(tp)
        self.nmi = self.calcNMI()
        self.jaccard = self.calcJaccard()
        print(str(self.nmi)+" "+str(self.jaccard))
        

    def calcNMI(self):
        G = [item[0] for item in self.inArray] 
        C = [item[1] for item in self.inArray] 
        cCounter = dict(collections.Counter(C))
        gCounter = dict(collections.Counter(G))
        allCounter = dict(collections.Counter(str(elem) for elem in self.inArray))

        #Calculate entropy of clusters
        entC = 0
        for ckey in cCounter:
            ci = cCounter[ckey]
            term = ci/self.n*math.log(ci/self.n,math.e)
            entC = entC - term #default in natural log
        #Calculate entropy of ground truth
        entG = 0
        for gkey in gCounter:
            gi = gCounter[gkey]
            entG = entG - gi/self.n*math.log(gi/self.n,math.e) #default in natural log
        #Calculate mutual information
        entMut=0
        for allKey in allCounter:
            muti = allCounter[allKey]
            coordList = allKey.strip('][').split(', ')
            gCoord = float(coordList[0])
            cCoord = float(coordList[1])
            gSum = gCounter[gCoord]
            cSum = cCounter[cCoord]
            entMut += (muti/self.n)*math.log((muti/self.n)/(gSum/self.n*cSum/self.n))

        self.nmi = entMut/(math.sqrt(entC*entG))
        return self.nmi
        
    def calcJaccard(self):
        pass
        
    def formatInputArray(self,tp):
        if(tp=="code"): #Read input with pandas from text file for testing.
            nrows_ = 100
            df = pd.read_csv(self.inputFilename,header=None,sep="\n")#,nrows = nrows_)
            df = df[0].str.split(" ",expand=True)
            df = df.astype(float)
            listVals = df.values.tolist()
            self.inArray = listVals
        if(tp=="hack"):
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
        self.n = len(self.inArray)
        '''Puts array values in self.inArray'''
        



def main():
    file = "mp5_clustEval\\sample1.txt"
    kmeans = aggCluster(file)
    kmeans.runPipe("clusters.txt","code")


if __name__=="__main__":
    main()