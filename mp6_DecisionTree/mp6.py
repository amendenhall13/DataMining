import pandas as pd
import numpy as np
import math
import collections

class DecisionTree(object):
    def __init__(self,file):
        

    def runPipe(self,output,tp):
        self.outFilename = output
        self.formatInputArray(tp)
        self.test = ""
        self.train = ""
        

    def classifyVals(self):
        pass

    def findSplit(self):
        pass

    def calcInfoGain(self):
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
    file = "mp5_clustEval\\sample2.txt"
    dTree = DecisionTree(file)
    dTree.runPipe("clusters.txt","code")


if __name__=="__main__":
    main()