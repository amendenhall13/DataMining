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

    def runPipe(self,outputFilename,nrows_):
        self.outputFilename = outputFilename
        #verticalDF = self.readTextFile(self.filepath,nrows)
        #verticalDF.to_excel("vertical.xlsx")
        verticalDF = pd.read_csv("mp2_ContSeqPatterns\\vertical.csv",nrows=nrows_)
        singles = verticalDF["word"].unique()
        for i,sing in enumerate(singles):
            singles[i] = np.array([singles[i]])
        print(singles)
        #Start test vals
        #self.minAbsSup=4
        #testDF = pd.read_csv("mp2_ContSeqPatterns\\test.csv",nrows=nrows_)
        #testCand = np.array([["zero","one"],["four","five"]])
        #End test vals
        dict = self.calculateSupport(verticalDF,singles)
        print(dict)
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

    def calculateSupport(self,df,candidates):
        '''working function to calculate support given a numpy array of candidates and a vertical DF'''
        dict = {}

        for cand in candidates:
            mappedDFList = []
            for word in cand:
                filteredDF = df[df["word"]==word] #filter to just that word
                mappedDFList.append(filteredDF)

            mergedDF = mappedDFList[0] #Automatically assign first element.
            mergedDF = mergedDF.rename(columns={"EID":"EID_"+cand[0]})
            mergedDF = mergedDF.drop(columns="word")
            print(mergedDF)
            for idx,mDF in enumerate(mappedDFList[1:]): #Merge on SID and "word", idx off by one bc already assigned first one
                mDF = mDF.rename(columns={"EID":("EID_"+cand[idx+1])})
                mDF = mDF.drop(columns="word")
                #Merge mDF to mergedDF
                mergedDF = mergedDF.merge(mDF,how='inner',on="SID")
                #Filter out non-sequential ones (this one minus one before it ==1)
                mergedDF = mergedDF[mergedDF["EID_"+cand[idx+1]]-mergedDF["EID_"+cand[idx]]==1]
            support = mergedDF.nunique()["SID"]
            dict[tuple(cand)] = support
        return dict


                

    
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
    contSeqPat.runPipe("patterns.txt",100) #outputname,nrows (10,000 total in this example)

def test():
    pass

if __name__ == "__main__":
    main()
