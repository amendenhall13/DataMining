import pandas as pd
import numpy as np
import math

class aggCluster:
    def __init__(self,file):
        self.n = -1
        self.k = -1
        self.m = -1
        self.inArray = []
        self.outFilename = ""
        self.inputFilename = file
        self.clusters = []

    def runPipe(self,output,tp):
        self.outFilename = output
        self.formatInputArray(tp)
        clus = self.findClusters()
        self.clusters = clus

    def findClusters(self):
        '''Takes the 2D list and 3 parameters as inputs and returns a list of which cluster'''
        points = self.inArray
        clusters = []
        #Initialize each point into its own cluster
        for i in range(0,len(self.inArray)):
            clusters.append(i)
        
        distMatrix = []
        #Create distMatrix
        for ir,r in enumerate(range(len(points))):
            distMatrix.append([])
            for ic,c in enumerate(range(len(points))):
                distMatrix[ir].append(-1)
        #Calculate distances
        for i1, pt1 in enumerate(range(len(points))):
            for i2,pt2 in enumerate(range(len(points))):
                if(pt1 != pt2):
                    dist = self.calcDist(points[i1],points[i2])
                    distMatrix[i1][i2] = dist
        #print("distMatrix")
        #print(distMatrix)
        maxDist = max(max(distMatrix))
        minDist = min(min(distMatrix))
        #Create Cluster Matrix
        clustMatrix = []
        for ir,r in enumerate(range(len(clusters))):
            clustMatrix.append([])
            for ic,c in enumerate(range(len(clusters))):
                clustMatrix[ir].append(-1)
    
        #temp = 0
        #Loop through for clustering
        while len(set(clusters)) > self.k:
            #print("loop")
            #update clustMatrix by link type
            if self.m == 0:
                #Single link (min)
                for ir,r in enumerate(clusters):
                    for ic,c in enumerate(clusters):
                        clustMatrix[ir][ic] = -1
                #Fill Cluster matrix
                for ir,r in enumerate(clusters):
                    for ic,c in enumerate(clusters):
                        if(r != c): #don't compare same cluster
                            if(clustMatrix[r][c] == -1): #if hasn't been visited yet, use val
                                clustMatrix[r][c] = distMatrix[ir][ic]
                            elif(distMatrix[ir][ic]<clustMatrix[r][c]):
                                clustMatrix[r][c] = distMatrix[ir][ic]
                            else:
                                pass
                #print(clustMatrix)
            elif self.m == 1:
                #complete link (max)
                for ir,r in enumerate(clusters):
                    for ic,c in enumerate(clusters):
                        clustMatrix[ir][ic] = -1
                #Fill Cluster matrix
                for ir,r in enumerate(clusters):
                    for ic,c in enumerate(clusters):
                        if(r != c): #don't compare same cluster
                            if(clustMatrix[r][c] == -1): #if hasn't been visited yet, use val
                                clustMatrix[r][c] = distMatrix[ir][ic]
                            elif(distMatrix[ir][ic]>clustMatrix[r][c]):
                                clustMatrix[r][c] = distMatrix[ir][ic]
                            else:
                                pass
                #print(clustMatrix)
            else:
                #Average link
                for ir,r in enumerate(clusters):
                    for ic,c in enumerate(clusters):
                        clustMatrix[ir][ic] = -1
                countMatrix = [] #used to store number of 
                for ir,r in enumerate(range(len(clusters))):
                    countMatrix.append([])
                    for ic,c in enumerate(range(len(clusters))):
                        countMatrix[ir].append(0)
                #Fill Cluster matrix and count matrix
                for ir,r in enumerate(clusters):
                    for ic,c in enumerate(clusters):
                        if(r != c): #don't compare same cluster
                            if(clustMatrix[r][c] == -1): #if hasn't been visited yet, use val
                                clustMatrix[r][c] = distMatrix[ir][ic]
                                countMatrix[r][c] +=1
                            else:
                                clustMatrix[r][c] = (clustMatrix[r][c]+distMatrix[ir][ic])
                                countMatrix[r][c] +=1
                
                for ir,r in enumerate(clustMatrix):
                    for ic,c in enumerate(r):
                        if(c!=-1) and (countMatrix[ir][ic]!=0):
                            clustMatrix[ir][ic] = c/countMatrix[ir][ic]
                #print(clustMatrix)
                #print(countMatrix)
            #Find min value and row/col index to find clusters to merge
            minRow = -1
            minCol = -1
            minVal = maxDist
            for ir, r in enumerate(clustMatrix):
                for ic,val in enumerate(r):
                    if ((val != -1) and (val<minVal)):
                        minVal = val
                        minRow = ir
                        minCol = ic
            #print(minVal)
            #print(minRow)
            #print(minCol)
            #Merge the clusters associated with that value.
            '''merge clusters'''
            minClust = min(minRow,minCol)
            for i,clus in enumerate(clusters):
                if((clus == minRow) or (clus == minCol)):
                    clusters[i] = minClust
            #print(clusters)
            #temp +=1
        for i in clusters:
            print(i)
        




    def calcDist(self,p1,p2):
        '''Returns the distance between 2 points given'''
        return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

    def formatInputArray(self,tp):
        if(tp=="code"): #Read input with pandas from text file for testing.
            nrows_ = 100
            df = pd.read_csv(self.inputFilename,header=None,sep="\n")#,nrows = nrows_)
            df = df[0].str.split(" ",expand=True)
            self.n = int(df.iloc[0][0])
            self.k = int(df.iloc[0][1])
            self.m = int(df.iloc[0][2])
            df = df.iloc[1:,[0,1]]
            df = df.astype(float)
            listVals = df.values.tolist()
            self.inArray = listVals
        if(tp=="hack"):
            inpt = input()
            vals = inpt.split()
            self.n = int(vals[0])
            self.k = int(vals[1])
            self.m = int(vals[2])
            inArray = []
            for row in range(0,self.n):
                temp = input()
                separate = temp.split()
                separate[0] = float(separate[0])
                separate[1] = float(separate[1])
                inArray.append(separate)
            self.inArray = inArray
        '''Puts array values in self.inArray'''
        



def main():
    file = "mp4_heirarchical\\sample1.txt"
    kmeans = aggCluster(file)
    kmeans.runPipe("clusters.txt","code")


if __name__=="__main__":
    main()