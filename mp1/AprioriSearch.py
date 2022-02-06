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
import itertools

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
        #while(k <= 3): #self.melt["EID"].max()+1):
        candidates = self.generateCandidates(freqk,k)
        #Calculates support for candidates and adds ones with high enough support to self.freqSet along with their support.
        self.evaluateCandidates(candidates)
        print(self.freqSet)
        self.dictToTxt(self.freqSet)
            #k +=1

    def generateCandidates(self,freq,k):
        freqKminus1 = {}
        #find all of the length-1 patterns
        for item in freq:
            if len(item) == (k-1): #if freq k-1 patteern
                freqKminus1[item] = freq[item] #add to ones to generate from
        
        freqK = []
        #Create all combination of the keys with k-2 overlap
        for item1 in freqKminus1:
            for item2 in freqKminus1:
                if ((item1 != item2) and (item1) and (item2) ): #Don't merge same items, can't do single sets
                    if(k>2):
                        print(list(itertools.combinations(item1,k-2)))
                    else:
                        if( ((item1,item2) not in freqK) and ((item2,item1) not in freqK) ):
                            if(item1 < item2):
                                freqK.append((item1[0],item2[0]))
                            else:
                                freqK.append((item2[0],item1[0]))
                else:
                    pass#print("same set")
        return freqK


        

    def evaluateCandidates(self,candidates):
        candDict = {}
        for cand in candidates:
            support = self.calculateSupport(cand)
            if support >= self.minAbsSup:
                self.freqSet[cand] = support
                candDict[cand] = support

    def calculateSupport(self,cand):
        sup = 0
        for transaction in self.raw:
            if set(cand).issubset(transaction):
                sup +=1
        print(str(cand)+" "+str(sup))
        return sup


    def findk1Cand(self):
        counts = Counter(self.melt["category"])
        keys = counts.keys()
        for c in counts:
            if (counts[c] >= self.minAbsSup) and (c not in self.freqSet):
                self.freqSet[(c,)] = counts[c]
        self.dictToTxt(self.freqSet)
        
    def readTextFile(self,filepath):
        df = pd.read_csv(filepath,header=None,sep="\n")#,nrows = 1000)
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
                formattedKey+=k+";"
            formattedKey = formattedKey[:-1] #remove trailing semicolon
            file.write("%s:%s\n"%(value,formattedKey))


def main():
    file = "mp1\categories.txt"
    apriori = AprioriPipeline(file)
    apriori.runPipe("patterns.txt")

def test():
    file = "mp1\categories.txt"
    apri = AprioriPipeline(file)
    apri.readTextFile(file)
    support = apri.calculateSupport(("Pizza","Restaurants"))
    print("support"+str(support))

if __name__ == "__main__":
    main()


