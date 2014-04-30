# -*- coding: utf-8 -*-

import cv2
import numpy as np
import scipy as sp
import math
import os


IMAGE_PATH = '/Users/johnkelly/Pictures/IMG_4457/'
MIN_MATCH_COUNT = 10

def main():

    '''
    files = [f for f in os.listdir(IMAGE_PATH + 'resize/') if f[-4:]=='.jpg']
    
    img0 = cv2.imread(IMAGE_PATH + '/resize/' + files[0])
    '''
 
    cap = cv2.VideoCapture(IMAGE_PATH + 'IMG_4457.mov')
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    framecount = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
    width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
          
    print framecount,width,height,fps
            
    # Define the codec and create VideoWriter object
    fps = 25
    capSize = (width,height) # this is the size of my source video
    fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v') # note the lower case
    vout = cv2.VideoWriter()
    success = vout.open(IMAGE_PATH + 'stabilized/output.mov',fourcc,fps,capSize,True)
       
    retval,img1 = cap.read()   
    cumulativeM = np.identity(3)
    img2 = 1
    while not (img2==None):
                    
        pos = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
                            
        retval,img2 = cap.read()
        
        print pos
        
        #Initiate SIFT detector
        sift = cv2.SIFT()

        kp1,des1 = sift.detectAndCompute(img1,None)
        kp2,des2 = sift.detectAndCompute(img2,None)
    

    
        bf = cv2.BFMatcher(normType = cv2.NORM_L1, crossCheck = False)
    
        # Match descriptors.
        matches = bf.knnMatch(queryDescriptors=des1,trainDescriptors=des2,k=2)
    

    
        # Apply ratio test
        good = []
        for m,n in matches:
            if m.distance < 0.6*n.distance:
                good.append(m)

        #print len(kp1),len(kp2),len(good)
        
        
        #Find best fit transformation that maps img1 onto img2
        if len(good)>MIN_MATCH_COUNT:
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

            M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC,5.0)
            cumulativeM = np.dot(cumulativeM,M)
            transformedframe = cv2.warpPerspective(img2, cumulativeM, (img2.shape[1],img2.shape[0]))
                        
            # write the flipped frame
            vout.write(transformedframe)
            
            img1 = img2

        else:
            print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
            break



    cap.release()
    vout.release() 
    vout = None



if __name__=="__main__":
    
    main()
