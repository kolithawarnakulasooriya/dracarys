import cv2
import numpy as np

class ColorImageEnhancer(object):
    """
        this will contain enhance functionalities
    """

#   =======================================================================
# enhance the image using Equalize histogram methodology

    def EqualizeHistogram(self,imgGrayscale):
        return cv2.equalizeHist(imgGrayscale)

#   =======================================================================
#Top Hat Difference

    def MorPhological_Stretching(self,imgGrayscale):

        """
            Morpological stretched Image
            @params = original grayscale image
            @return = stretched gray scale image
        """
        height, width = imgGrayscale.shape

        imgTopHat = np.zeros((height, width, 1), np.uint8)
        imgBlackHat = np.zeros((height, width, 1), np.uint8)

        structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        imgTopHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_TOPHAT, structuringElement)
        imgBlackHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_BLACKHAT, structuringElement)
        imgGrayscalePlusTopHat = cv2.add(imgGrayscale, imgTopHat)
        imgGrayscalePlusTopHatMinusBlackHat = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

        return imgGrayscalePlusTopHatMinusBlackHat

#   =======================================================================

     
    def extractValue(self,imgOriginal):

        """
            extract value componant from HSV image
            @params = original BGR image
            @return = V componant of image of all pixels

        """
        height, width, numChannels = imgOriginal.shape
        imgHSV = np.zeros((height, width, 3), np.uint8)
        imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)
        imgHue, imgSaturation, imgValue = cv2.split(imgHSV)
        return imgValue

#   =======================================================================


    def extractHSV(self,imgOriginal):

        """
            extract H,S,V componants from BGR image

            @params = original BGR image
            @return = H, S, V componants of image of all pixels

        """

        height, width, numChannels = imgOriginal.shape
        imgHSV = np.zeros((height, width, 3), np.uint8)
        imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)
        imgHue, imgSaturation, imgValue = cv2.split(imgHSV)
        return imgHue, imgSaturation, imgValue

#   =======================================================================
    

    def extractRGB(self,imgOriginal):

        """
            extract R,G,B componants from BGR image

            @params = original BGR image
            @return = R,G,B componants of image of all pixels

        """

        height, width, numChannels = imgOriginal.shape
        imgRGB = np.zeros((height, width, 3), np.uint8)
        imgRGB = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2RGB)
        imgR, imgG, imgB = cv2.split(imgRGB)
        return imgR, imgG, imgB




