import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


class Kmeans:
    def __init__(self,file):
        self.k = 3
        self.file = file
        self.X = ""
        self.clusters = []
        self.outputFilename = ""

    def runPipe(self,output):
        self.outputFilename = output
        self.formatInputArray()
        kmeans = KMeans(n_clusters=self.k, random_state=0).fit_predict(self.X)
        print(kmeans)
        self.clusters = kmeans
        self.formatOutput()


    def formatInputArray(self):
        nrows_ = 100
        df = pd.read_csv(self.file,header=None,sep="\n")#,nrows = nrows_)
        df = df[0].str.split(",",expand=True)
        arr = df.to_numpy()
        self.X = arr

    def formatOutput(self):
        file = open(self.outputFilename,"w")
        print(type(self.clusters))
        for i,val in enumerate(self.clusters):
            print(i)
            file.write("%s %s\n"%(i,val))
        



def main():
    file = "mp3_kmeans\\places.txt"
    kmeans = Kmeans(file)
    kmeans.runPipe("clusters.txt")


if __name__=="__main__":
    main()