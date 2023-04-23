
import numpy as np
import sys
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

def makeGaussian(size, sigma):
    # Initializing value of x-axis and y-axis from -1 to 1
    x, y = np.meshgrid(np.linspace(-1,1,size), np.linspace(-1,1,size))
    gauss = np.exp(-((x*x+y*y)/ (2.0 * sigma**2))) / (2*np.pi*sigma**2)
    return gauss

def histogram_eq(img2d):
    row,col=img2d.shape
    buff2d = img2d.copy()
    histo = np.full(256,0)
    pdf = cdf = np.full(256,0.0)
    for i in range(row):
        for j in range(col):
            histo[int(buff2d[i][j])] += 1
    for i in range(256):
        pdf[i] = histo[i]/(row*col)
        if i == 0:
            cdf[i] = pdf[i]
        else:
            cdf[i] = cdf[i-1]+pdf[i]
    for i in range(row):
        for j in range(col):
            img2d[i][j] = intlimit(255.0*cdf[buff2d[i][j]])
    return


# Smoothing Filters
def smoothing(img2d, msize, type = 'average', sigma = 1):
    # prepare buffer
    buff2d = img2d.copy()
    row, col = img2d.shape
    hs = int(msize/2)  # half_size
    
    if type == 'average':
        mask = np.full((msize,msize), 1/(msize**2))  # make masks
        for i in range(hs,row-hs):                   # do smoothing
            for j in range(hs,col-hs):
                piece = buff2d[i-hs : i+hs+1, j-hs : j+hs+1]
                img2d[i][j] = intlimit(np.sum(piece * mask))

    elif type == 'gaussian':
        mask = makeGaussian(msize, sigma)  # shape, fill_value
        for i in range(hs,row-hs):             # do smoothing
            for j in range(hs,col-hs):
                piece = buff2d[i-hs : i+hs+1, j-hs : j+hs+1]
                img2d[i][j] = intlimit(np.sum(piece * mask))

    elif type == 'median':
        for i in range(hs,row-hs):          # do smoothing
            for j in range(hs,col-hs):
                piece = buff2d[i-hs : i+hs+1, j-hs : j+hs+1]
                img2d[i][j] = np.median(piece, axis = None)
    else:
        print("Wrong Filter Name! Original image is returned.")

    return

# Sharpening Filters
def sharpening(img2d, type):
    buff2d = img2d.copy()
    row, col = img2d.shape
    hs = int(3/2)   # derivative filter is set to only 3*3

    if type == 'sobel':
        gx_mask = np.array([[-1,0,1], [-2,0,2],[-1,0,1]])
        gy_mask = np.array([[-1,-2,-1],[0,0,0], [1,2,1]])

        for i in range(hs,row-hs):                   # do smoothing
            for j in range(hs,col-hs):
                piece = buff2d[i-hs : i+hs+1, j-hs : j+hs+1]
                gx = np.sum(piece * gx_mask)
                gy = np.sum(piece * gy_mask)
                img2d[i][j] = intlimit(np.sqrt(gx**2 + gy**2))
        return

    elif type == 'laplacian1':
        mask = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]])
    elif type == 'laplacian2':
        mask = np.array([[0,1,0],[1,-4,1],[0,1,0]])
    elif type == 'laplacian3':
        mask = np.array([[1,1,1],[1,-8,1], [1,1,1]])
    elif type == 'laplacian4':
        mask = np.array([[-1,-1,-1],[-1,8,-1], [-1,-1,-1]])
    else:
        print("Wrong Filter Name! Original image is returned.")
        return
    
    for i in range(hs,row-hs):                   # do smoothing
        for j in range(hs,col-hs):
            piece = buff2d[i-hs : i+hs+1, j-hs : j+hs+1]
            img2d[i][j] = intlimit(img2d[i][j] - np.sum(piece * mask))

    return



if __name__ == '__main__':
    # receive input image
    img_name = input("Input file name: ")
    if img_name=="":
        img_name="clock_noise2.bmp"
        print(f"Default file:{img_name}")
    
    # change to grayscale image
    im = Image.open(img_name)
    cimg3d = np.array(im)
    gimg2d = np.full(im.size,0)
    color3dtogray2d(cimg3d,gimg2d)

    # receive the desired action
    job = input("You mant to do [hist/filter]:")

    if job == "filter" :    
        # set the filter type
        smooth_filters = ['average','gaussian', 'median']
        sharp_filters = ['sobel', 'laplacian1','laplacian2', 'laplacian3', 'laplacian4']
        print("available filter types are: \n average, gaussian, median, sobel, laplacian[1,2,3,4]")
        while(True):
            filter_type = input("Input filter type: ")
            sigma = 0
            if(filter_type in smooth_filters+sharp_filters):
                if filter_type == "gaussian":
                    sigma = float(input("give the distribution of gaussian: "))
                break
            elif filter_type == "":
                filter_type = "average"
                print(f"Default file:{filter_type}")
                break
            else:
                print("Wrong filter name. Please give proper filter name")
    
        # set the mask filter size
        if filter_type in smooth_filters:
            msize_str = input("Input mask size (row):")
            if msize_str=="":
                msize=3
                print(f"Default mask size (row):{msize}")
            else:
                msize=int(msize_str)
        else:
            msize = 3
            print(f"Default mask size (row):{msize}")

        # Image filtering
        if filter_type in smooth_filters:
            smoothing(gimg2d, msize, filter_type, sigma)
        elif filter_type in sharp_filters:
            sharpening(gimg2d, filter_type)

        if filter_type == "gaussian":
            out_img_name = filter_type + str(sigma) + "_" + str(msize) + '_' + img_name
        else:
            out_img_name= filter_type + "_" + str(msize) + '_' + img_name

    elif job == "hist": # histogram equalize
        histogram_eq(gimg2d)
        out_img_name= "histogramEq_" + img_name

    else:
        print("Wrong job!")
        sys.exit(0)

    # change back to color image
    gray2dtocolor3d(gimg2d,cimg3d)

    im2=Image.fromarray(cimg3d)
    im2.save(out_img_name)