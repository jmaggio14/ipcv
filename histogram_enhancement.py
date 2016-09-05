import ipcv
from sys import exc_info
import numpy as np


def histogram_enhancement(img, etype='linear2', target=None, maxCount=255):
    # try: 
    if isinstance(img, np.ndarray) == False:
        print("input 'img' must be a numpy.ndarray | currently is {0}".format(type(img)))
    elif (img.dtype != np.uint8) and (img.dtype != np.float32):
        print("input 'img' must either be np.uint8 or np.float32")
        print("currently is {0}".format(img.dtype))


    histByBand = {}; pdfByBand = {}; cdfByBand = {}
    print(img.shape)
    for band in range(img.shape[2]):
        histByBand[band],pdfByBand[band],cdfByBand[band] = ipcv.histogram(img=img,\
                                                                            channels=[band],\
                                                                            histSize=[maxCount+1],\
                                                                            ranges=[0,maxCount+1],\
                                                                            returnType=1)

    if etype == "linear2" or etype == "linear1":
        print(etype[-1])
        lowerBound,upperBound = float( etype[-1] ) / 2.0

    elif etype == 'equalize':
        cdf = sum(cdfByBand.values) / len(cdfByBand)
        LUT = ( (cdf - cdf.min()) * maxCount ) / ( cdf.max()- cdf.min() )
        LUT = LUT.astype(np.uint8)
        img = LUT[img]

    return img
    # except Exception as e:
    #     print("----------------------------------------------")
    #     print("unable to compute because: {0} on line {1}".format(e,exc_info()[-1].tb_lineno))
    #     print("----------------------------------------------")


    # REFERENCE FROM OPENCV DOCS http://bit.ly/2bSSPqF
    # cdf_m = np.ma.masked_equal(cdf,0)
    # cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
    # cdf = np.ma.filled(cdf_m,0).astype('uint8')



if __name__ == '__main__':

    import cv2
    import ipcv
    import os.path
    import time

    home = os.path.expanduser('~')
    filename = home + os.path.sep + 'src/python/examples/data/redhat.ppm'
    # filename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'
    # filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
    # filename = home + os.path.sep + 'src/python/examples/data/giza.jpg'

    # matchFilename = home + os.path.sep + 'src/python/examples/data/giza.jpg'
    # matchFilename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
    # matchFilename = home + os.path.sep + 'src/python/examples/data/redhat.ppm'
    # matchFilename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'

    im = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    print('Filename = {0}'.format(filename))
    print('Data type = {0}'.format(type(im)))
    print('Image shape = {0}'.format(im.shape))
    print('Image size = {0}'.format(im.size))

    cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename, im)

    # print('Linear 2% ...')
    # startTime = time.time()
    # enhancedImage = ipcv.histogram_enhancement(im, etype='linear2')
    # print('Elapsed time = {0} [s]'.format(time.time() - startTime))
    # cv2.namedWindow(filename + ' (Linear 2%)', cv2.WINDOW_AUTOSIZE)
    # cv2.imshow(filename + ' (Linear 2%)', enhancedImage)

    # print('Linear 1% ...')
    # startTime = time.time()
    # enhancedImage = ipcv.histogram_enhancement(im, etype='linear1')
    # print('Elapsed time = {0} [s]'.format(time.time() - startTime))
    # cv2.namedWindow(filename + ' (Linear 1%)', cv2.WINDOW_AUTOSIZE)
    # cv2.imshow(filename + ' (Linear 1%)', enhancedImage)

    print('Equalized ...')
    startTime = time.time()
    enhancedImage = ipcv.histogram_enhancement(im, etype='equalize')
    print('Elapsed time = {0} [s]'.format(time.time() - startTime))
    cv2.namedWindow(filename + ' (Equalized)', cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename + ' (Equalized)', enhancedImage)

    # tgtIm = cv2.imread(matchFilename, cv2.IMREAD_UNCHANGED)
    # print('Matched (Image) ...')
    # startTime = time.time()
    # enhancedImage = ipcv.histogram_enhancement(im, etype='match', target=tgtIm)
    # print('Elapsed time = {0} [s]'.format(time.time() - startTime))
    # cv2.namedWindow(filename + ' (Matched - Image)', cv2.WINDOW_AUTOSIZE)
    # cv2.imshow(filename + ' (Matched - Image)', enhancedImage)

    # tgtPDF = numpy.ones(256) / 256
    # print('Matched (Distribution) ...')
    # startTime = time.time()
    # enhancedImage = ipcv.histogram_enhancement(im, etype='match', target=tgtPDF)
    # print('Elapsed time = {0} [s]'.format(time.time() - startTime))
    # cv2.namedWindow(filename + ' (Matched - Distribution)', cv2.WINDOW_AUTOSIZE)
    # cv2.imshow(filename + ' (Matched - Distribution)', enhancedImage)

    action = ipcv.flush()