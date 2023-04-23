# Segmentation (threshilding, sobel filtering, morphological filtering, region growing, region labeling, region selection)
# feature extraction
# recognition (Bayes classifier, template matching)

import os,time
import numpy as np
from numpy import median
from PIL import Image
from matplotlib import pyplot as plt

def Sobel(img):
    buff = img.copy()
    row, col = img.shape
    hs = int(3/2)

    gx_mask = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    gy_mask = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    for i in range(hs, row-hs):
        for j in range(hs, col-hs):
            piece = buff[i-hs : i+hs+1, j-hs:j+hs+1]
            gx = np.sum(piece*gx_mask)
            gy = np.sum(piece * gy_mask)
            img[i][j] = np.sqrt(gx**2+gy**2)
    img = np.where(img < 0, 0, img)
    img = np.where(img > 255, 255, img)
    return img

def thresholding(img, th_low, th_high): 
    # threshold intensities to zero! wherelse orange
    img = np.where(img < th_low, 0, img)
    img = np.where(img > th_high, 255, img)
    return img

def c_thresholding(img):
    l = (160, 40,0)
    h = (255, 255, 100)

    row = img.shape[0]
    col = img.shape[1]
    gimg = gimg = np.full((row, col), 0)
    for i in range(row):
        for j in range(col):
            r = img[i][j][0]
            g = img[i][j][1]
            b = img[i][j][2]
            if(r < l[0] or r > h[0] or g < l[1] or g > h[1] or b > h[2]):
                pass
            else:
                gimg[i][j] = 255
            # if (img[i][j][0] - img[i][j][2] > 90) and (img[i][j][0] - img[i][j][1] < 170):
            #     gimg[i][j] = 0
            #     #gimg[i][j] = int(0.299*img[i][j][0]+0.587*img[i][j][1]+0.114*img[i][j][2])
    return gimg


def Segmentation(imgtype, img, imgpath, saveflag):
    # thresholding
    if imgtype == "gray": # Grayscale
        # Sobel filter
        # out = Sobel(img)
        # Thresholding
        th_low = 40
        th_high = 60
        out = thresholding(img, th_low, th_high)
    
    else:                   # color
        # color thresholding
        out = c_thresholding(img)

    # # Region based
    # out = regionSeg(img=img, threshold=35)

    # Save
    if(saveflag == True):
        out = np.where(out < 0, 0, out)
        out = np.where(out > 255, 255, out)
        out=np.uint8(out)
        im=Image.fromarray(out)

        im.save(imgpath)
    return out


if __name__ == "__main__":
    path1 = '/content/drive/MyDrive/cimg'
    path = '/content/drive/MyDrive/cimg/sobel'
    imagePaths = [os.path.join(path, imgs) for imgs in os.listdir(path)]

    for imgpath in os.listdir(path):
        if imgpath.endswith(('jpeg', 'png', 'jpg')):
            # load image
            img_source = Image.open(os.path.join(path, imgpath)) #.convert('L')   # to grayscale
            img = np.array(img_source, 'uint8')

            # Segmentation
            seg_out = Segmentation('gray', img, os.path.join(path1, f'gseg/th{imgpath}'), True)
