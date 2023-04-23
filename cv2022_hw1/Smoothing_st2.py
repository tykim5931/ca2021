import numpy as np
from numpy import median
from PIL import Image

def intlimit(val):  # filter pixel value to represent image correctly.
    if val>255:
        val=255
    elif val<0:
        val=0
    return round(val)

def color3dtogray2d(cimg,gimg): # change color image(dimension3) to gray image(dimension2)
    row,col=gimg.shape
    for i in range(row):
        for j in range(col):
            gimg[i][j]=int(0.299*cimg[i][j][0]+0.587*cimg[i][j][1]+0.114*cimg[i][j][2])

def gray2dtocolor3d(gimg,cimg): # change from gray to color
    row,col=gimg.shape
    for i in range(row):
        for j in range(col):
            for k in range(3):
                cimg[i][j][k]=gimg[i][j]

def maskfiltering(img2d,mask):  
    buff2d=img2d.copy()
    row,col=img2d.shape
    ms=int(len(mask)/2) # mask must be square with odd dimension.
    
    for i in range(ms,row-ms):
        for j in range(ms,col-ms):
            sum=0.0
            for p in range(-ms,ms+1):
                for q in range(-ms,ms+1):
                    sum+=buff2d[i+p][j+q]*mask[p+ms][q+ms]
            img2d[i][j]=intlimit(sum)

def medianfiltering1(img2d,ms):
    buff2d=img2d.copy()
    row,col=img2d.shape
    hs=int(ms/2) # mask must be square with odd dimension.
    
    for i in range(hs,row-hs):
        for j in range(hs,col-hs):
            temp = []
            for p in range(-hs,hs+1):
                for q in range(-hs,hs+1):
                    temp.append(buff2d[i+p][j+q])
            temp.sort()
            img2d[i][j]=temp[int(ms*ms/2)]

#################### main procedure starts here
img_name = input("Input file name: ")
if img_name=="":
    img_name="clock_speckle.bmp"
    print(f"Default file:{img_name}")

msize_str = input("Input mask size (row):")
if msize_str=="":
    msize=3
    print(f"Default mask size (row):{msize}")
else:
    msize=int(msize_str)

im = Image.open(img_name)
col, row = im.size

cimg3d = np.array(im)
gimg2d = np.full((row,col),0)

color3dtogray2d(cimg3d,gimg2d)

mask=np.full((msize,msize),1/(msize*msize))  # average mask

'''
std = 2.0
hs=int(msize/2) # msize must be odd number
for i in range(-hs,hs+1):
    for j in range(-hs,hs+1):
        mask[i+hs][j+hs] = (1.5/hs)*(1.0/(2*3.1416*std))*np.exp(-1.0*(i*i+j*j)/(2*std*std))

#(1.5/hs) is an arbitaray constant for better visualizaiotion.
'''

maskfiltering(gimg2d,mask)

#medianfiltering1(gimg2d,msize)

gray2dtocolor3d(gimg2d,cimg3d)

#out_img_name="out_gaussian_mask"+str(msize)+"_std"+str(std)+img_name
out_img_name="out_average_mask"+str(msize)+img_name
im2=Image.fromarray(cimg3d)
im2.save(out_img_name)