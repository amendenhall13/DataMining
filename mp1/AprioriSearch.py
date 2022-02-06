#Implementation of Apriori Algorithm
''' for k = 1 to max length
1. Find all k-1 frequent items
2. Make all k patterns from them
3. Find frequency of all generated k-length patterns
4. k+1 and repeat until no more found.
'''
import pandas as pd
import numpy as np
import math
from collections import Counter

class AprioriPipeline(object):
    def __init__(self,filepath_):
        self.filepath = filepath_
        self.raw = pd.DataFrame()
        self.melt = pd.DataFrame()
        self.freqSet = {}
        self.minAbsSup = 771 #reset in readTextFile
        self.minRelSup = 0.01
        self.outputFilename = ""


    def runPipe(self,outputFilename):
        self.outputFilename = outputFilename
        self.melt = self.readTextFile(self.filepath)
        self.findk1Cand() #updates self.freqSet with the set of k=2 freq items
        self.apriori() #updates self.freqSet with the set of frequent items found
        
    def apriori(self):
        freqk = self.freqSet
        k = 2
        while(k <= self.melt["EID"].max()+1):
            candidates = self.generateCandidates(freqk,k)
            #Calculates support for candidates and adds ones with high enough support to self.freqSet along with their support.
            self.evaluateCandidates(candidates)
            k +=1

    def generateCandidates(self,freq,k):
        freqKminus1 = {}
        #find all of the length-1 patterns
        for item in freq:
            if len(item) == (k-1): #if freq k-1 patteern
                freqKminus1[item] = freq[item] #add to ones to generate from
        

    def evaluateCandidates(self,candidates):
        pass
        '''calculate support of candidates
        if support is greater than the min, add to freqset'''


    def findk1Cand(self):
        counts = Counter(self.melt["category"])
        keys = counts.keys()
        for c in counts:
            if (counts[c] >= self.minAbsSup) and (c not in self.freqSet):
                self.freqSet[(c,)] = counts[c]
        self.dictToTxt(self.freqSet)
        
    def readTextFile(self,filepath):
        df = pd.read_csv(filepath,header=None,sep="\n")
        listDF = df[0].str.split(";",expand=True)
        self.minAbsSup = math.floor(self.minRelSup*listDF.shape[0])
        list = listDF.values.tolist()
        listSeries = pd.Series(list)
        self.raw = listSeries
        listDF["TID"] = listDF.index
        meltDF = pd.melt(listDF,id_vars=["TID"],var_name="EID",value_name="category")
        meltDF = meltDF.dropna()
        return meltDF
    
    def dictToTxt(self,dict):
        file = open(self.outputFilename,"w")
        for key, value in dict.items():
            formattedKey = ""
            for k in key:
                formattedKey=k+";"
            formattedKey = formattedKey[:-1] #remove trailing semicolon
            file.write("%s:%s\n"%(value,formattedKey))


def main():
    file = "mp1\categories.txt"
    apriori = AprioriPipeline(file)
    apriori.runPipe("patterns.txt")


if __name__ == "__main__":
    main()

