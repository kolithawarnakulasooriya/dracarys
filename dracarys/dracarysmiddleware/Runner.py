from imagepreprocessor  import ImagePreProcessor
from areapredictor import AreaPredictor
import numpy as np
import sys

class Runner(object):
    """
        Developed by Kolitha Warnakulasooriya

        Run the identification process here

                    (StokePoint)
                ___ | ___
              /     |    \
             /      |     \
            /       |      \
           |        |       \
    -------------------------------------
 (LeftMarginalPoint)|    (RightMarginalPoint)
                    |
                    |
                    |
    """

    SPLIT_RANGE = 2
    UPPER_MARGINE = 5

    StokePoint = (-1,-1)
    LeftMarginalPoint =  (-1,-1)
    RightMarginalPoint =  (-1,-1)


    def __init__(self, sourceImage):
        
        imp = ImagePreProcessor.ImagePreProcessor(sourceImage)
        
        self.grayscaleThreshold = imp.proecss() # get enhanced grayscale image
        
        # read first boundary point list

        areaPredictor = AreaPredictor.AreaPredictor(self.grayscaleThreshold,self.SPLIT_RANGE)
        boundaryPoints = areaPredictor.getPointList()

        while True:

            # get the first boundary point values

            _,_,y = self.getDifferedValues(boundaryPoints[0])   

            if(y < self.UPPER_MARGINE): # if upper row is above upper margie 
                break;

            # find slice points untill previous upper point

            areaPredictor = AreaPredictor.AreaPredictor(self.grayscaleThreshold,self.SPLIT_RANGE,y)
            
            # if point list dows not contain matched points 
            if(areaPredictor.getPointList() == -1 or len(areaPredictor.getPointList())==0):
                break;
            
            # check points are having matched pattern. else reject
            boundaryPointsTemp = self.reAllocatePoints(areaPredictor.getPointList());

            # concatenate previous boundaries and filtered boundaries
            boundaryPoints = np.vstack((boundaryPointsTemp,boundaryPoints))
        

        # =============== Finish Filtering =================================

        # get the mid point
        h,w = self.grayscaleThreshold.shape
        midPoint = (w/2, h/2)

        #get the closest boundary points to mid
        centerPoint, lowerX, higherX = self.getClosestBoundaryPoints(midPoint, boundaryPoints)

        # get the mid of lowest x and higer x es
        midx1, midx2 = self.getMidXValues(boundaryPoints);

        # get Estimatd stoke point
        x1,x2,y1 = self.getDifferedValues(boundaryPoints[0])

        # get the Stoke X point finding mid of X es
        StokeX = (x1+x2)/2
        StokeY = y1

        # check if stoke point is in first half of the image, else -1

        if(StokeY < h/4):
            self.StokePoint = (StokeX, StokeY)

        self.LeftMarginalPoint = (midx1, centerPoint[1])    
        self.RightMarginalPoint = (midx2, centerPoint[1])



#   =======================================================================

    def getDifferedValues(self,point):
        """
            @return x1,x2,y
        """
        return point[0][0],point[1][0],point[0][1]

#   =======================================================================

    def reAllocatePoints(self,points):

        """
            filter points which are in extract pattern, rearreange mis filtered slice values

            @params:
                list of slice points ((x1,y),(x2,y))

            @return 
                list of filtered slice points ((x1,y),(x2,y))
        """

        resultedPoints = []

        for i in points:

            # if result point has no points, first point must add for compare
            if(len(resultedPoints) ==0):
                resultedPoints.append(i)
                continue

            # get the last filtered point 
            lx1,lx2,_ = self.getDifferedValues(resultedPoints[-1])

            # current point
            cx1,cx2,y = self.getDifferedValues(i)

            # check lowest point , must bigger than previous
            if cx1>lx1:
                cx1=lx1

            # check highest point , must lesser than previous
            if cx2<lx2:
                cx2 = lx2

            resultedPoints.append(((cx1,y),(cx2,y)))

        return resultedPoints


#   =======================================================================

    def getClosestBoundaryPoints(self,midPoint, boundaryPoints):

        """
            get the closest points for the given point

            @params:
                midPoint : fixed point use to compare
                boundaryPoints : set of points 

            @return:
                center point(x,y), lowest x position, higher x position
        """
        minimum_distance = sys.maxint
        
        # if boundary points empty
        if len(boundaryPoints) == 0:
            return -1,-1,-1

        # get the minimum distance to mid point
        for bpoint in boundaryPoints:

            distance = (bpoint[0][1] - midPoint[1])**2
            
            if(distance< minimum_distance):
                minimum_distance = distance
                centerBoundaryPoint = bpoint
        
        centerY = centerBoundaryPoint[0][1]
        centerX = (centerBoundaryPoint[0][0] + centerBoundaryPoint[1][0])/2
        return (centerX,centerY),centerBoundaryPoint[0][0] , centerBoundaryPoint[1][0]

#   =======================================================================


    def getMidXValues(self, boundaryPoints):

        """
            mid values of boundary point X es

            @params:
                point list
            @return:
                mid x value of lowest x points,  mid x value of highest x points
        """
        # total x values / number of x values
        midX1 =0
        midX2 =0

        for i in boundaryPoints:

            x1, x2,_ = self.getDifferedValues(i)

            midX1 += x1
            midX2 += x2

        l = len(boundaryPoints)

        return midX1/l , midX2/l 