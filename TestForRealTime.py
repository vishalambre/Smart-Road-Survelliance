import cv2
import numpy as np
import time
# import sys
# import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *


def srs():
    ip = cv2.VideoCapture(IPVIDEONAME)
    bgsubtractor = cv2.BackgroundSubtractorMOG()
    count = 0
    kernel = np.ones((5, 5), np.uint8)
    PAUSE = False

    y,e=0,0 #Setting Defaults to avoid Errors

    while ip.isOpened():
        ret, img = ip.read()
        if ret:
            copy = img.copy()
            img = cv2.blur(img, (5, 5))
            cv2.imshow("Blur",img)


            # Setting Imaginary Lines and points to check
            ############################################################################################################
            if LINE_ORIENTATION=="Vertical Reference Line":
                #HardCoded Points
                ##################################################################################################################################
                cv2.line(img, (img.shape[1] / 2, 0), (img.shape[1] / 2, img.shape[0]), (255, 127, 0), 2)
                cv2.line(img, (img.shape[1] / 2+50, 0), (img.shape[1] / 2+50, img.shape[0]), (255, 127, 0), 2)
                pt1 = img.shape[1] / 2
                pt2 = img.shape[1] / 2 + 50
                ################################################################################################################################

                #Using DISTBETWEENPOINTS variable
                ########################################################################################################################################
                # cv2.line(img, (img.shape[1] / 2-DISTBETWEENPOINTS/2, 0), (img.shape[1] / 2-DISTBETWEENPOINTS/2, img.shape[0]), (255, 127, 0), 2)
                # cv2.line(img, (img.shape[1] / 2 + DISTBETWEENPOINTS/2, 0), (img.shape[1] / 2 + DISTBETWEENPOINTS/2, img.shape[0]), (255, 127, 0), 2)
                # pt1=img.shape[1] / 2-DISTBETWEENPOINTS/2
                # pt2=img.shape[1] / 2 + DISTBETWEENPOINTS/2
                ######################################################################################################################################




            else:
                cv2.line(img, (0, img.shape[0] / 2), (img.shape[1], img.shape[0] / 2), (255, 127, 0), 2)
                cv2.line(img, (0,img.shape[0] / 2 -50), (img.shape[1], img.shape[0]/2-50), (255, 127, 0), 2)

                pt2 = img.shape[0] / 2-50  #Swapped pt1 and pt2 positons not tested
                pt1=  img.shape[0] / 2
            ############################################################################################################


            # Preprocessing the Video
            ############################################################################################################
            imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            backsubimg = bgsubtractor.apply(imggray, None, 0.01)
            # cv2.imshow("BGSubImg",backsubimg)
            dilate = backsubimg

            for i in range(9):
                dilate = cv2.erode(dilate, None, iterations=1)
                dilate = cv2.dilate(dilate, None, iterations=2)

            dilate = cv2.erode(dilate, None, iterations=1)
            # cv2.imshow("Erode",dilate)
            ############################################################################################################



            # Finding Countours and Drawing them
            ############################################################################################################
            contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # cv2.imshow('After Contouring', dilate)
            # cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
            for c in contours:
                (x,y,w,h)=cv2.boundingRect(c)
                # cv2.line(test, (img.shape[0]/2,0), (img.shape[0]/2,img.shape[1]), (255, 127, 0), 2)
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                M = cv2.moments(c)
                if M["m00"] != 0:                       #Fixed Divide By Zero Error
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                else:
                    cx, cy = 0, 0
                #print(cx,xofline)

                if LINE_ORIENTATION=="Vertical Reference Line":
                    if cx > pt1 and cx < pt1 + 10:
                        e=time.time()
                        count = count + 1
                        print count
                        if cv2.contourArea(c)>=MWR1 and cv2.contourArea(c)<=MWR2:
                            print "Medium Weighted Vehicle"
                        else:
                            print "Heavy Weighted Vehicle"

                    if cx>pt2 and cx<pt2+5:
                        print("coincide")
                        s=time.time()
                        y=s-e
                        speed=20/y
                        print speed,"km/h"
                        if(speed>SPEED_LIMIT):
                            name = "Snaps\\"+"ID"+str(count)+" "+str(speed)+" "+"kmph"+".jpg"
                            crop_img = copy[int(y):int(y+w+100),int(x):int(x+h+100)]
                            cv2.imwrite(name,crop_img)

                else:
                    if cy>=pt1 and cy<=pt1+3:
                        e = time.time()
                        count=count+1
                        print count

                        if cv2.contourArea(c)>=MWR1 and cv2.contourArea(c)<=MWR2:
                            print "Medium Weighted Vehicle"
                        else:
                            print "Heavy Weighted Vehicle"

                    if cx>pt2 and cx<pt2+5:
                        # print("coincide")
                        s=time.time()
                        y=s-e
                        speed=DISTBETWEENPOINTS/y
                        print speed,"km/h"
                        if(speed>SPEED_LIMIT):
                            name = "Snaps\\"+"ID"+str(count)+" "+str(speed)+" "+"kmph"+".jpg"
                            crop_img = copy[int(y):int(y+w+100),int(x):int(x+h+100)]
                            cv2.imwrite(name,crop_img)



            ############################################################################################################


             # Drawing Centroids
             ###########################################################################################################
                cv2.circle(img, (cx, cy), 3, (255, 0, 255), -1)
                cv2.imshow("Detected Vehicles", img)
            ############################################################################################################


            # Mechanism for sustaining pause,play,nextFrame which is set in the outer while loop
            ############################################################################################################
            while (PAUSE):
                k = cv2.waitKey()
                # print(k)
                if k == 32:  # PAUSE Video Using Spacebar
                    PAUSE = False

                if k == 13:  # Next Frame Using Enter
                    break

                if k == 27:  # Exit When in Paused State using ESC
                    PAUSE = False
                    break
            ############################################################################################################

            # Setting FPS and pause state
            ############################################################################################################
            k = cv2.waitKey(30)
            if k == 27:
                break
            if k == 32:
                PAUSE = True
            ############################################################################################################

        # If no next frame is available i.e ret is false
        ################################################################################################################
        else:
            print("Video Ended")
            break
        ###############################################################################################################

    ip.release()
    cv2.destroyAllWindows()



if __name__=='__main__':

    # Setting parameters global that are required to run
    global IPVIDEONAME, LINE_ORIENTATION, SPEED_LIMIT, MWR1, MWR2, DISTBETWEENPOINTS

    # Setting the defaults for the variables for console application
    ####################################################################################################################
    IPVIDEONAME = 0
    LINE_ORIENTATION="Vertical Reference Line"
    SPEED_LIMIT=60
    MWR1=0
    MWR2=60
    DISTBETWEENPOINTS=20
    #####################################################################################################################


    # Calling the main logic function
    srs()


    # Connection from GUI
def valueSetter(window,browsefile, referenceline, t1, t2, t3, t4, dropbox,t5,t6):

    #Setting parameters global that are required to run
    global IPVIDEONAME, LINE_ORIENTATION, SPEED_LIMIT, MWR1, MWR2, DISTBETWEENPOINTS

    #Flag if all is good to go
    READYTOGO=True


    # Setting values from GUI
    #####################################################################################################################
    try:
        IPVIDEONAME=str(browsefile)
        LINE_ORIENTATION = str(referenceline)
        SPEED_LIMIT = int(t6)
        MWR1 = int(t1)
        MWR2 = int(t2)
        DISTBETWEENPOINTS=int(t5)

    except ValueError:
        READYTOGO = False
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("ERROR")
        msg.setText("Please specifiy all numeric inputs")
        msg.setStandardButtons(QMessageBox.Ok)
        # msg.buttonClicked.connect(sys.exit)
        retval = msg.exec_()


    ####################################################################################################################

    # Handling if File is not Selected
    ####################################################################################################################
    if str(browsefile)=='No file selected':
        READYTOGO=False
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("ERROR")
        msg.setText("Select a File or WebCam")
        msg.setStandardButtons(QMessageBox.Ok)
        # msg.buttonClicked.connect(sys.exit)
        retval=msg.exec_()
    ####################################################################################################################

    elif str(browsefile)=='WebCam Selected':
        IPVIDEONAME = 0

    if READYTOGO:
        srs()