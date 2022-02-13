import pandas as pd
import numpy as np
import math
from collections import Counter
import itertools

class ContSeqPatPipeline(object):
    def __init__(self,filepath_):
        self.filepath = filepath_
        self.raw = pd.DataFrame()
        self.melt = pd.DataFrame()
        self.freqSet = {}
        self.minAbsSup = 100 #reset in readTextFile
        self.minRelSup = 0.01
        self.outputFilename = ""

    def runPipe(self,outputFilename,nrows):
        self.outputFilename = outputFilename
        #verticalDF = self.readTextFile(self.filepath,nrows)
        #verticalDF.to_excel("vertical.xlsx")
        verticalDF = pd.read_excel("mp2_ContSeqPatterns7\vertical.xlsx")
        #self.findk1Cand() #updates self.freqSet with the set of k=2 freq items
        #self.apriori() #updates self.freqSet with the set of frequent items found
        dict = {} 
        self.dictToTxt(dict)


    def readTextFile(self,filepath,nrows_):
        '''Read in the file and transform to vertical format'''
        df = pd.read_csv(filepath,header=None,sep="\n",nrows = nrows_)
        #Transform into vertical data format to use spade
        rawDF = df[0].str.split(" ",expand=True)
        self.minAbsSup = math.floor(self.minRelSup*rawDF.shape[0])
        vertDF = pd.DataFrame(columns=["word","SID","EID"])
        for rowIndex,row in rawDF.iterrows():
            for colIndex,value in row.items():
                if value != None:
                    vertDF = vertDF.append({"word":value, "SID":rowIndex,"EID":colIndex},ignore_index=True)
                else:
                    print("None: "+ str(value))
                    print(rowIndex)  
        return vertDF

    
    def dictToTxt(self,dict):
        '''Transform a dict into a text file.'''
        file = open(self.outputFilename,"w")
        for key, value in dict.items():
            formattedKey = ""
            for k in key:
                formattedKey+=k+";"
            formattedKey = formattedKey[:-1] #remove trailing semicolon
            file.write("%s:%s\n"%(value,formattedKey))



def main():
    file = "mp2_ContSeqPatterns\\review_samples.txt"
    contSeqPat = ContSeqPatPipeline(file)
    contSeqPat.runPipe("patterns.txt",10000) #outputname,nrows (10,000 total in this example)

def test():
    pass

if __name__ == "__main__":
    main()
