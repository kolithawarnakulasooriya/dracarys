from dracarys.dracarysmiddleware.Runner  import Runner

def Execute(sourceImage, area):

    """
        Execution of Process Dracarys Middleware

        @params:
            sourceImage = RGB Imagecomes from the camera
            area= interested area of the cucumber  
                  (
                    start position ,
                    end position ,
                    cropped box width,
                    cropped box height
                  )
        @return: touple of
                 (
                    left position point (x,y),
                    right position point (x,y),
                    center stoke position point(x,y)
                 )
        
                    
    """

    colorImage = getColorROI(sourceImage,area);
    runner = Runner(colorImage)

    return runner.StokePoint, runner.LeftMarginalPoint, runner.RightMarginalPoint


def getColorROI(image,area):

    """
        Make the ROI of sourceimage

        @params image   = source image
                area    = ROI position informaton
    """

    if area==0:
        return image    # if area == 0 no cropping function attached

    # find start position and end position of the ROI area

    start_x = area[0]
    start_y = area[1]

    end_x =  start_x + area[2] 
    end_y =  start_y + area[3]

    # image[r:r+h , c:c+w] ROI image and return
    return image[start_y:end_y, start_x:end_x]