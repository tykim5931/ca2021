# Segmentation ( threshilding, sobel filtering, morphological filtering, region growing, region labeling, region selection)
# feature extraction
# recognition (Bayes classifier, template matching)

import os,time
import numpy as np
from numpy import median
from PIL import Image
from matplotlib import pyplot as plt


       
def merge(i, j, i_, j_, pl, th, reg, reginfo):  # it does not perform merging between regions which should follow later.
    
    reg[i][j][0]=pl

    if reg[i_][j_][0]==pl: 
        reginfo[int(pl)][0]+=1
        reginfo[int(pl)][1]=(reginfo[int(pl)][1]*(reginfo[int(pl),0]-1)+reg[i,j,1])/reginfo[int(pl)][0]
    
    if reg[i_][j_][0]!=pl: # in case of second merging after merging once with upper or left pixel.
        
        row, col = reg.shape[:2]

        old=reg[i_][j_][0]
        reg[i_][j_][0]=pl

        reginfo[int(pl)][0]+=1
        reginfo[int(pl)][1]=(reginfo[int(pl)][1]*(reginfo[int(pl)][0]-1)+reg[i_][j_][1])/reginfo[int(pl)][0]
        reginfo[int(old)][0]-=1
        
        if reginfo[int(old)][0]<=0:
            reginfo[int(old)][0]=0
            reginfo[int(old)][1]=0 
        else:
            reginfo[int(old)][1]=(reginfo[int(old)][1]*(reginfo[int(old)][0]+1)-reg[i_][j_][1])/reginfo[int(old)][0]
    
        old=int(old)
        pl=int(pl)
        
        if old == pl or reginfo[old][1]-reginfo[pl][1] > th:
            # print(f"Merging {old} and {pl} failed.\n-Diff is",reginfo[old][1]-reginfo[pl][1])
            return 0
        else:
            if old < pl:
                m,n=old,pl
            else:
                m,n=pl,old

            reginfo[m][0] += reginfo[n][0]
            reginfo[m][1] = (reginfo[m][1]*reginfo[m][0]+reginfo[n][1]*reginfo[n][0])/(reginfo[m][0]+reginfo[n][0])

            reginfo[n][0]=0
            reginfo[n][1]=0
            # print(f"Merging {old} and {pl} happened")

            for u in range(row):
                for v in range(col):
                    if  reg[u][v][0]==n:
                            reg[u][v][0] = m
                            reg[u][v][1] = reginfo[m][1]
        
    return (reg, reginfo)


def separate(i, j, img, rct, reg, reginfo):
    rct+=1
    reg[i][j][0]=rct
    reginfo[int(rct)][0]+=1
    reginfo[int(rct)][1]= img[i][j]
    return (rct, reg, reginfo)


def picklarge(img,info,n):
    row,col=img.shape
    
    regareasort=np.full(row*col,0)
    reglabelsort=np.full(n+1,0)
    outimg=np.full((row,col),255)

    for i in range(row*col):
        regareasort[i]=info[i][0]
    
    regareasort=np.sort(regareasort)[::-1]
    
    for i in range(n):
        for j in range(row*col):
            if regareasort[i]==info[j][0]:
                reglabelsort[i]=j

    for i in range(row):
        for j in range(col):
            for k in range(n):
                if img[i][j]==reglabelsort[k]:
                    outimg[i][j]=reglabelsort[k]
                    #outimg[i][j]=0
    return outimg 


def relabeling(rct, regions, region_info):
    row, col = regions.shape[:2]
    ct=0
    reglabel = np.full((row*col,3),0.0)

    for i in range(rct+1):
        if region_info[i][0]!=0:
            ct=ct+1
            reglabel[ct][0]=region_info[i][0]
            reglabel[ct][1]=region_info[i][1]
            reglabel[ct][2]=i # to save old label

    for i in range(rct+1):
            region_info[i][0]=reglabel[i][0]
            region_info[i][1]=reglabel[i][1]

    newreg=np.full((row,col,2),0.0)

    for i in range(row):
        for j in range(col):
            ol=regions[i][j][0]
            for k in range(rct+1):
                if reglabel[k][2]==ol:
                    newreg[i][j][0]=k
                    newreg[i][j][1]=reglabel[k][1]

    for i in range(row):
        for j in range(col):
                regions[i][j][0]=newreg[i][j][0]
                regions[i][j][1]=newreg[i][j][1]
    return (rct, regions, region_info)