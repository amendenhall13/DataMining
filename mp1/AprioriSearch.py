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
        self.freqSet = {}
        self.minAbsSup = 771 #reset in readTextFile
        self.minRelSup = 0.01


    def runPipe(self,outputFilename):
        self.raw = self.readTextFile(self.filepath)
        self.findk1Cand() #updates self.freqSet with the set of k=2 freq items
        self.apriori() #updates self.freqSet with the set of frequent items found
        
    def apriori(self):
        freqk = self.freqSet
        k = 1
        '''while(freqk not empty):
            ckplus1 = candidates
            find fk+1
            k+=1
        '''

    def findk1Cand(self):
        counts = Counter(self.raw["category"])
        keys = counts.keys()
        for c in counts:
            if (counts[c] >= self.minAbsSup) and (c not in self.freqSet):
                self.freqSet[c] = counts[c]
        print(self.freqSet)
        
        


    def readTextFile(self,filepath):
        df = pd.read_csv(filepath,header=None,sep="\n")
        listDF = df[0].str.split(";",expand=True)
        self.minAbsSup = math.floor(self.minRelSup*listDF.shape[0])
        listDF["TID"] = listDF.index
        meltDF = pd.melt(listDF,id_vars=["TID"],var_name="EID",value_name="category")
        meltDF = meltDF.dropna()
        return meltDF
    


def main():
    file = "mp1\categories.txt"
    apriori = AprioriPipeline(file)
    apriori.runPipe("patterns.txt")


if __name__ == "__main__":
    main()

