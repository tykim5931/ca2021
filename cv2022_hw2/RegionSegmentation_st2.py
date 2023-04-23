import os,time
import numpy as np
from numpy import median
from PIL import Image
from matplotlib import pyplot as plt

def intlimitimg(img2d):
    row,col=img2d.shape
    for i in range(row):
        for j in range(col):
            if img2d[i][j]>255:
                img2d[i][j]=255
            elif img2d[i][j]<0:
                img2d[i][j]=0
    return img2d            

def color3dtogray2d(cimg,gimg):
    global row, col
    for i in range(row):
        for j in range(col):
            gimg[i][j] = int(0.299*cimg[i][j][0]+0.587*cimg[i][j][1]+0.114*cimg[i][j][2])

def writeimage2d(img,name):
    row,col = img.shape
    img = np.where(img < 0, 0, img)
    img = np.where(img > 255, 255, img)
    # intlimitimg(img)

    img=np.uint8(img)
    im=Image.fromarray(img)
    im.save(name)
    return im
       
def merge(i,j,ii,jj,pl):  # it does not perform merging between regions which should follow later.
    global rct, reg, reginfo
    
    reg[i][j][0]=pl

    if reg[ii][jj][0]==pl: 
        reginfo[int(pl)][0]+=1
        reginfo[int(pl)][1]=(reginfo[int(pl)][1]*(reginfo[int(pl)][0]-1)+reg[i][j][1])/reginfo[int(pl)][0]
    
    if reg[ii][jj][0]!=pl: # in case of second merging after merging once with upper or left pixel.
        old=reg[ii][jj][0]
        reg[ii][jj][0]=pl
        reginfo[int(pl)][0]+=1
        reginfo[int(pl)][1]=(reginfo[int(pl)][1]*(reginfo[int(pl)][0]-1)+reg[ii][jj][1])/reginfo[int(pl)][0]
        reginfo[int(old)][0]-=1
        
        if reginfo[int(old)][0]<=0:
            reginfo[int(old)][0]=0
            reginfo[int(old)][1]=0 
        else:
            reginfo[int(old)][1]=(reginfo[int(old)][1]*(reginfo[int(old)][0]+1)-reg[ii][jj][1])/reginfo[int(old)][0]
        
        mergeregion(old,pl)
        
def mergeregion(l1, l2):
    global reg, reginfo, rct, row, col
    l1=int(l1)
    l2=int(l2)
    
    if l1 == l2 or reginfo[l1][1]-reginfo[l2][1] > th:
        print(f"Merging {l1} and {l2} failed.\n-Diff is",reginfo[l1][1]-reginfo[l2][1])
        return 0
    else:
        if l1 < l2:
            m,n=l1,l2
        else:
            m,n=l2,l1

        reginfo[m][0] += reginfo[n][0]
        reginfo[m][1] = (reginfo[m][1]*reginfo[m][0]+reginfo[n][1]*reginfo[n][0])/(reginfo[m][0]+reginfo[n][0])

        reginfo[n][0]=0
        reginfo[n][1]=0
        print(f"Merging {l1} and {l2} happened")

        for u in range(row):
            for v in range(col):
                if  reg[u][v][0]==n:
                        reg[u][v][0] = m
                        reg[u][v][1] = reginfo[m][1]
    
        return 1

def separate(i,j):
    global inimg, rct, reg, reginfo
    rct+=1
    reg[i][j][0]=rct
    reginfo[int(rct)][0]+=1
    reginfo[int(rct)][1]=inimg[i][j]
    

def relabeling():
    global reg,row, col, rct, reginfo
    ct=0
    reglabel = np.full((row*col,3),0.0)

    for i in range(rct+1):
        if reginfo[i][0]!=0:
            ct=ct+1
            reglabel[ct][0]=reginfo[i][0]
            reglabel[ct][1]=reginfo[i][1]
            reglabel[ct][2]=i # to save old label

    for i in range(rct+1):
            reginfo[i][0]=reglabel[i][0]
            reginfo[i][1]=reglabel[i][1]

    newreg=np.full((row,col,2),0.0)

    for i in range(row):
        for j in range(col):
            ol=reg[i][j][0]
            for k in range(rct+1):
                if reglabel[k][2]==ol:
                    newreg[i][j][0]=k
                    newreg[i][j][1]=reglabel[k][1]

    for i in range(row):
        for j in range(col):
                reg[i][j][0]=newreg[i][j][0]
                reg[i][j][1]=newreg[i][j][1]


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


# main procedure starts here
os.system('cls' if os.name=='nt' else 'clear')  # clear screen
start = time.time()

#inimg= [[  0,  0, 0, 255, 255],\
#        [  0,  0, 0, 255, 255],\
#        [  0,  0, 0, 255, 255],\
#        [  255, 255, 255, 0, 0],\
#        [  255,  0, 0, 0, 0]] 

#inimg=[[ 9,  8,  8,  8,  0],\
#       [10,  3,  6,  8,  5],\
#       [10,  7, 10,  4,  7],\
#       [ 7,  5,  5,  3,  5],\
#       [ 5,  8,  5,  3,  5]]
#inimg=np.array(inimg)
#row,col = inimg.shape

#row,col=5,5
#inimg=np.random.rand(row,col)
#inimg=np.uint8(np.round(inimg*10))

#print("Input:\n",inimg)


#img_name = input("Input file name: ")
if True: #img_name=="":
    img_name="bsc256.bmp"
    print(f"Default file:{img_name}")
im = Image.open(img_name)
col,row = im.size
cimg3d = np.array(im)
inimg = np.full((row,col),0)
color3dtogray2d(cimg3d,inimg)

reg=np.full((row,col,2),0.0)  #reg[i][j][0] is label value of pixel (i,j), and reg[i][j][1] is updated intensity of pixel (i,j)
reginfo = np.full((row*col,2),0.0) #reginfo[i][0] is the pixel count of region label i, and reginfo[i][1] is updated intensity of region label i
reg[0][0][0]=1  # The label starts from 1 for first region
rct=0
#th = 2.5
th=30

for i in range(row):
    for j in range(col):
        reg[i][j][1]=inimg[i][j]

for i in range(row):
    for j in range(col):  # upper first and left next makes a better result as low label is prioritized.
 
        rowmerge=colmerge=0
        
        if i!=0 and abs(inimg[i][j] - reginfo[int(reg[i-1][j][0])][1]) <= th:
            merge(i,j,i-1,j,reg[i-1][j][0])
            rowmerge=1
               
        if j!=0 and abs(inimg[i][j] - reginfo[int(reg[i][j-1][0])][1]) <= th:
            if rowmerge!=1:
                merge(i,j,i,j-1,reg[i][j-1][0]) # in case of col merge without prior row merge
                colmerge=1
            else: # in case of col merge after prior row merge
                if reg[i-1][j][0]!=reg[i][j-1][0]:  # to exclude duplicate merging for the same label upper and left pixels
                    if abs(inimg[i][j] - reginfo[int(reg[i][j-1][0])][1]) <= th*0.5:
                        merge(i,j,i,j-1,reg[i-1][j][0])  # if rowmerge already happened, pl is set to previous rowmerge
                        colmerge=1
                                    
            if i!=0 and rowmerge==0 and abs(reginfo[int(reg[i][j][0])][1] - reginfo[int(reg[i-1][j][0])][1]) <= th*0.5: # After colmerge, if rowmerge becomes possible.
                merge(i,j,i-1,j,reg[i][j-1][0]) # in case that colmerge happens, pl is set to previous colmerge
                rowmerge=1
            
        if rowmerge==0 and colmerge==0:
            separate(i,j)
     
relabeling()
outregl=reg[:,:,0].copy().reshape(row,col)
outregi=reg[:,:,1].copy().reshape(row,col)

outregl2=picklarge(outregl,reginfo,7)

#print("Region label:\n",outregl)
#print("Region intensity:\n",np.round(outregi,2))
#print("Region info:\n",np.round(reginfo[:rct+1,:],2))
#print("Selected region labels:\n",outregl2)

im=writeimage2d(outregl2,"out_largest_bsc256.bmp")
im.show()
stop = time.time()
print("time taken:",stop-start)

