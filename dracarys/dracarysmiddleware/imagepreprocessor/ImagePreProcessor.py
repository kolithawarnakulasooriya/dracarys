import ColorImageEnhancer, ColorImageEnhancer
import numpy as np
import cv2


GAUSSIAN_SMOOTH_FILTER_SIZE = (5,5)

class ImagePreProcessor(ColorImageEnhancer.ColorImageEnhancer):
    """
        Pre process the image befor execution

    """

    def __init__(self, sourceImage):
        
        self.imgSource = sourceImage
        super(ColorImageEnhancer.ColorImageEnhancer, self).__init__()
#   =======================================================================


    def proecss(self):
        value = self.extractValue(self.imgSource);     # get the gray values of image
        enhanced = self.EqualizeHistogram(value)  # enhance the color contrast
        enhanced = self.MorPhological_Stretching(enhanced)    # enhance the border contrast
        imgPreprocessed =  self.__getBluredImage(enhanced)                    # 
        return imgPreprocessed

#   =======================================================================


    def __getBluredImage(self,source):

        """
            get the Blued image 
            @params = original grayscale image
            @return = blurred gray scale image
        """
        height, width = source.shape    # extract the shape h, w
        imgBlurred = np.zeros((height, width, 1), np.uint8) # create empty image
        imgBlurred = cv2.GaussianBlur(source,GAUSSIAN_SMOOTH_FILTER_SIZE, 0)
        return imgBlurred
