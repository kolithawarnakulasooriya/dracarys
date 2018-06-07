import math
from scipy.fftpack import rfft
from scipy import integrate,signal
import numpy as np


class AreaSlize(object):
    """
        Slice the image with intensities

        +-----------------------+
        |                       |
      -----------------------------------  Slize 1 (x[] , y, intensities[])
        |                       |
        |                       |
        |                       |
    

        |
        |   -
        |  -  -
        | -    - <= intensities
        |- 
        |
        ________<= x coordinate

         @params : 
            xintensities= set of intensity values along to x coordinations
            y = sliced Y coordination         
         @return = Area Slize Object
    """ 

    def __init__(self, xintensities, y):

        self.intensities = xintensities # set of intensity values along to x coordinations
        self.y = y                      # sliced Y coordination

        self.curveCoeffs = self.getfittedCurveCoefficients();  # set fo fitted curve coeficient values to set of intensities

#   =======================================================================

    def getfittedCurveCoefficients(self):

        """
            fit a curve to intensity datapoints on the area slice.
       
            @return = set of coefficients of the curve equation
        """

        cols = [i for i,_ in enumerate(self.intensities)]
        coeffs = np.polyfit(cols,self.intensities, 6) # fit a curve like Ax^6 + Bx^5 + Cx^4 + Dx^3 + Ex^2 + Fx + G

        return np.poly1d(coeffs)    # return coefficients with poly1d equation

#   =======================================================================

    def getFreqChanges(self,areaSlizes):

        """
           how much deviate a slice compared with current slice

           @params : set of AreaSliZe objets
           @params : set of meadiate error of curve frequencies
        """

        f1 = self.getFittedCurveFFT()   # get set of amplitudes accoring to the sampled frquencies for this curve
        f1 = self.normalize(f1)    # normalize the frequency values
        fx = np.power(f1,2)             # set of squres of frequency values

        errors = []                     # list of frequency amplitude errors

        for ar in areaSlizes:
            
            f2 = ar.getFittedCurveFFT() # get set of amplitudes accoring to the sampled frquencies AreaSlice object
            f2 = self.normalize(f2)# normalize the frequency values
            fy = np.power(f2,2)         # set of squres of frequency values
            d = np.subtract(fx,fy)      # difference of frequencies
            d = abs(np.sum(d))          # sum of all freqiency changes 
            errors.append(d)            

        return errors

#   =======================================================================

    def getFittedCurveFFT(self):

        """
            get the fitted curve frequencis with real part of Discrete fourier transformation
            
            @return set of discreate frequencies(real part)
        """
        arr = np.array(self.getFittedCurveValues())
        return rfft(arr)

#   =======================================================================


    def getFittedCurveValues(self):

        """
            get a curve intensity values according to each and every x points

            @return set of curved intensity points 
        """
        curveIntensityValues=[]

        for i in range(0, len(self.intensities)):
            curveIntensityValues.append(self.curveCoeffs(i))

        return curveIntensityValues

#   =======================================================================

    def normalize(self,arr):

        """
            nomalize the set of values

            @return normalized array
        """

        sum = np.sum(arr)            # sum of all values
        avg= sum / (len(arr)+0.0001) # get the avarage of all values(remove devide by 0)
        
        norm=[] # set of normal values
        for i in arr:
            norm.append(i/avg)

        return norm 

#   =======================================================================


    def getFirstLowerPointsFromMid(self):

        """
            extract the two closest minimum points arround the center point of samples

            @return lower minimum point from center, higher minimum point from center

        """

        # get the mid point of the scale
        mid_x = len(self.intensities)/2
        
        #get upper half and lower half
        upperHalf = []
        lowerHalf = []

        # extract upper half from mid point
        for i in range(mid_x,len(self.intensities)):
            upperHalf.append(self.intensities[i])

        # extract lower half from mid point
        for i in range(mid_x-1,-1,-1):
            lowerHalf.append(self.intensities[i])

        # get the next minimum point of upper x coordinate
        upperXCoordinate = self.getNextMidPoint(upperHalf)
        if upperXCoordinate == -1 :
            return -1 # if no codination found
        upperXCoordinate += mid_x   

        # get the next minimum point of lower x coordinate

        lowerXCoordinate = self.getNextMidPoint(lowerHalf)
        if lowerXCoordinate == -1:
            return -1 # if no codination found
        lowerXCoordinate = (mid_x -1) - lowerXCoordinate 
        
        return (lowerXCoordinate, upperXCoordinate)


#   =======================================================================


    def getNextMidPoint(self, pointList):

        """
            get next Lowest point from point list

        """

        arr = np.array(pointList)
        gradiants = np.array(self.__getGradientCode(arr))
        ref_code = -1
        for i in range(1,gradiants.size):
            p1= int(gradiants[i-1])
            p2= int(gradiants[i])

            mulp = p1 * p2
            add = p1+p2

            logic1 = mulp < 0 and add <= 0 and p1<0
            logic2 = mulp == 0 and add < 0 and p1<0
            logic3 = mulp ==0 and add > 0 and p1==0

            if logic1 or logic3:
                return i
            if logic2 :
                ref_code = i

        if(ref_code != -1):
            return ref_code
        return -1


#   =======================================================================

    def __getGradientCode(self,points):

        """
            get the curvature gradiants

            \ -1
            - 0
            / +1
        """
        gcods = []
        for i in range(1,points.size):
            p1 =int(points[i-1])
            p2 =int(points[i])
            
            point = p2-p1

            if(point < 0):
                gcods.append(-1)
            elif(point >0 ):
                gcods.append(+1)
            else:
                gcods.append(0)
        return gcods