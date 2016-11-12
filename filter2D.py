import numpy as np
import ipcv

def filter2D(src, dstDepth, kernel, delta=0, maxCount=255):
    """
    :NAME:
        filter2D

    :PURPOSE:
        this method applies a spatial filter to an image


    :CATEGORY:
        ipcv -- spatial filtering and modification tool

    :INPUTS:
        src
            [numpy.ndarray] input image
        dstDepth
            [IPCV type] the dtype of the dst array
        kernel
            [numpy.ndarray] the kernel to be applied to the image
        delta
            [int,float] offset to be added to the image
        maxCount
            [int] maximum value of the output image

    :RETURN VALUE:
        filtered image in the form of a numpy.ndarray 

    :ERROR CHECKING:
        ValueError
        TypeError

    :REQUIRES:
        numpy

    :MODIFICATION HISTORY:
        Engineer:   Jeff Maggio
        original:   10/12/2016

    """
    #ERROR CHECKING
    ipcv.type_check(src,np.ndarray,"src")
    # ipcv.type_check(dstDepth, ipcv.IPCV_TYPES,"dstDepth")
    ipcv.type_check(kernel,np.ndarray,"kernel")
    ipcv.type_check(delta, (int,float), "delta")
    ipcv.type_check(maxCount,(int,float),"maxCount")
    ipcv.value_check(maxCount,'b', (0,':'), "maxCount")

    try:
        
        #Converting to float64 (only if necessary)
        if src.dtype != ipcv.IPCV_64F:
            src = src.astype(ipcv.IPCV_64F)
        if kernel.dtype != ipcv.IPCV_64F:
            kernel = kernel.astype(ipcv.IPCV_64F)

        #Normalizing the kernel
        weight = np.sum(kernel)
        weight = 1.0 if weight == 0.0 else weight
        kernel = kernel / weight

        dst = np.zeros(src.shape)

        rowOffset = kernel.shape[0] // 2
        colOffset = kernel.shape[1] // 2
        
        src = np.roll(src,rowOffset, axis=0)
        src = np.roll(src,colOffset, axis=1)
        for element in range(kernel.size):
            dst = dst + (src * kernel.flat[element])
            src = np.roll(src, -1, axis = (element % 2) )


        dst = np.clip(dst + delta,0,maxCount) if (delta>0.0) else np.clip(dst,0,maxCount)
        return dst.astype(dstDepth) 

    except Exception as e:
        ipcv.debug(e)




if __name__ == '__main__':

    import cv2
    import os.path
    import time

    home = os.path.expanduser('~')
    filename = home + os.path.sep + 'src/python/examples/data/redhat.ppm'
    filename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'
    filename = home + os.path.sep + 'src/python/examples/data/checkerboard.tif'
    filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
    filename = home + os.path.sep + 'src/python/examples/data/lenna_color.tif'

    src = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

    dstDepth = ipcv.IPCV_8U
    kernel = np.asarray([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
    offset = 0
    # kernel = np.asarray([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
    # offset = 128
    # kernel = np.ones((15,15))
    # offset = 0
    # kernel = np.asarray([[1,1,1],[1,1,1],[1,1,1]])
    # offset = 0

    startTime = time.time()
    dst = ipcv.filter2D(src, dstDepth, kernel, delta=offset)
    print('Elapsed time = {0} [s]'.format(time.time() - startTime))

    cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename, src)

    cv2.namedWindow(filename + ' (Filtered)', cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename + ' (Filtered)', dst)

    action = ipcv.flush()
