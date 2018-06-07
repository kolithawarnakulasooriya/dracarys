import numpy as np
from dracarys.dracarysmiddleware.areapredictor.AreaSlize import AreaSlize

class AreaPredictor(object):
    """
        selected slizes of intensities of image

        @params : 
            source= grayscale image for processing
            n = next slice will captured after n-1 times of pixels
            endY = ending Y position from the top of the image.; if full image needs to slice then endY = -1
        @return = set of AreaSlize objects
    """

    def __init__(self, source, n, endY=-1):
        
        verticleAreaSlizes = self.getXangleAreaSlizes(source,n,endY)
        self. curvaturePointListVerticle = self.findCurvaturePointList(verticleAreaSlizes)
        
    def getPointList(self):
        return self.curvaturePointListVerticle

    def getXangleAreaSlizes(self,source,n, endY):

        """
            get the set of slices after slicing the image in horizontal peaces

             @params : 
                source= grayscale image for processing
                n = next slice will captured after n-1 times of pixels
                endY = ending Y position from the top of the image.; if full image needs to slice then endY = -1
             @return = set of AreaSlize objects
        """

        rows,cols = source.shape    # get rows and columns of the image
        numberOfcolomns = cols     
        areaSlizes = []             # list of slice objects

        #start slicing the area
        for i in range(rows):       # count from the top and row by row

            if(i%n==0 and i != 0):  # what is the row which should slize 

                vals = [val for _,val in enumerate(source[i])]  # get the list of Intensity Values for each row
                slize = AreaSlize(vals,i)             # make Slice object
                areaSlizes.append(slize)
            if endY != -1 and i == endY:    # return if the i th row equals to end row,
                break 

        return areaSlizes

#   =======================================================================

  
    def findCurvaturePointList(self,areaSlizes):

        """
            find the list of points which match the same border 

            @params:
                areaSlizes = list of AreaSlize objects
            @return:
                list of ((x1,y),(x2,y)) points 
        """

        meanSlizes = areaSlizes     # set of mean slices , befor decording
        lastLength =0

        while True: # do the same process until find best mean curve and best matching points

            # find the mean slice

            meanSlicePoints = self.getMeanSlicePoints(meanSlizes) 
            meanSlize = AreaSlize(meanSlicePoints,-1)     # create the mean slice using mean intensity points

            # get the set of avarage errors with compared to mean slice.

            curveDeviations = meanSlize.getFreqChanges(areaSlizes)
            
            # get the mean error as thethreshold point of slice

            ThresholdError = np.mean(curveDeviations)

            # filter AreaSlize Objects which the difference is lower than Threshold point

            filteredSlices = [] 

            for i in range(0, len(curveDeviations)-1):
                if(curveDeviations[i] <= ThresholdError):
                    filteredSlices.append(areaSlizes[i])
    
            # get the closest two min points arround mid sample position of mean curve

            firstLowerPointsFromMid = meanSlize.getFirstLowerPointsFromMid();
            if(firstLowerPointsFromMid == -1) :
                return -1
        
            # filterize the points from mean
            centerDistance =  abs(firstLowerPointsFromMid[0] - firstLowerPointsFromMid[1])
            meanSqreError = self.getMeanDistanceSqureError(filteredSlices,centerDistance)

            # extract points list
            pointList = self.extractPointListFromSlizes(filteredSlices,meanSqreError,centerDistance)
            # create Points

            meanSlizes = filteredSlices     # current slices is filterize slices

            # check the previous point list with current list. if it equals no need to proceed next
            l= len(filteredSlices)
            if(l - lastLength)==0:
                break

            lastLength = l  # set the previous length as current length

        return pointList

#   =======================================================================


    def getMeanSlicePoints(self,slizes):

        """
            find the mean of all intensities represent each x coordinate

            @return : set of mean intensity according to x coordinates
        """

        points = []
        l = len(slizes[0].intensities)

        for i in range(0,l):
            sp=[]
            for sl in slizes:
                sp.append(sl.intensities[i])

            arr = np.array(sp)
            points.append(np.mean(arr))

        return points

#   =======================================================================

    def getMeanDistanceSqureError(self,areaSlizes, centerdist):

        """
            find the mean error of AreaSlize Object , lower points with the specific diatance

            @params:
                areaSlizes = AreaSlize Objects
                centerdist = compaired distance

            @return:
                mean error
        """
        sumOfSqure =0
        count =0

        for i in areaSlizes:

            borderPoints = i.getFirstLowerPointsFromMid()   # get 2 lower points from the mid
            if borderPoints == -1 :                         # if no points found skip
                continue

            # get the distance of lower points
            borderDistance = abs(borderPoints[0] - borderPoints[1])

            # get the sqre of diatance error
            distanceError = borderDistance - centerdist
            distanceSqreError = distanceError ** 2

            #total errors
            sumOfSqure += distanceSqreError
            count += 1

        # get the avarage
        meanDistanceSqureError = sumOfSqure / count

        return meanDistanceSqureError

#   =======================================================================

    def extractPointListFromSlizes(self,areaSlices,thresholdError,centerDistance):

        """
            extract boundry point list from selected slice list
            
            @params:
                areaslices = list of AreaSlize obijects
                meanSqreError = filtering threshold error
                centerdistance = distance of 2 points which extractd from center slice
            
            @return 
                list of ((x1,y),(x2,y)) points 
        """
        pointList = list()

        for i in areaSlices:

            borderPoints = i.getFirstLowerPointsFromMid()    # get 2 lower points from the mid
            if borderPoints == -1 :                          # if no points found skip
                continue

            # get the distance of lower points
            borderPointsDistance = abs(borderPoints[0] - borderPoints[1])

            # get the sqre of diatance error
            borderDistanceError = borderPointsDistance - centerDistance
            borderDistanceSqreError = borderDistanceError ** 2 

            # filterize the slice point error with threshold error
            if borderDistanceSqreError < thresholdError :
                pointList.append(((borderPoints[0],i.y),(borderPoints[1],i.y))) # ((x1,y) , (x2,y))

        return pointList