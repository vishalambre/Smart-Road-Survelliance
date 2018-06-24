import cv2
import numpy as np
import time
import datetime
import sys
# import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Email import *

def srs():
    ip = cv2.VideoCapture(IPVIDEONAME)
    bgsubtractor = cv2.BackgroundSubtractorMOG()
    count = 'N/A'
    heavyweigthcount = 0
    mediumweigthcount = 0
    kernel = np.ones((5, 5), np.uint8)
    PAUSE = False
    Framecount=0
    fc1=0
    fc2=0
    y,e=0,0 #Setting Defaults to avoid Errors
    speed= "N/A"
    flagtostartlogic = False
    detectedVehicle = "N/A"
    if IPVIDEONAME==0:
        num_frames = 120;

        # print "Capturing {0} frames".format(num_frames)

        # Start time
        start = time.time()

        # Grab a few frames
        for i in xrange(0, num_frames):
            ret, frame = ip.read()

        # End time
        end = time.time()

        # Time elapsed
        seconds = end - start
        # print "Time taken : {0} seconds".format(seconds)

        # Calculate frames per second

        fps = num_frames / seconds

        print("fps",fps)
    else:
        fps = ip.get(cv2.cv.CV_CAP_PROP_FPS)
        print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)

    while ip.isOpened():
        ret, img = ip.read()
        if ret:
            copy = img.copy()

            # copy=cv2.resize(copy,(400,400))
            # img = cv2.resize(img, (400, 400))
            Framecount=Framecount+1
            timestamp = datetime.datetime.now()
            ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
            cv2.putText(copy, ts, (10, copy.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.55, (0, 0, 255), 1)
            # cv2.imshow("CCTV",copy)

            # Setting Imaginary Lines and points to check
            ############################################################################################################
            if LINE_ORIENTATION=="Vertical Reference Line":
                #HardCoded Points
                ##################################################################################################################################
                # pt1 = img.shape[1] / 2
                # pt2 = img.shape[1] / 2 + 100
                # cv2.line(copy, (pt1, 0), (img.shape[1] / 2, img.shape[0]), (255, 127, 0), 2)
                # cv2.line(copy, (pt2, 0), (img.shape[1] / 2+100, img.shape[0]), (255, 127, 0), 2)
                ################################################################################################################################

                #Using DISTBETWEENPOINTS variable
                ########################################################################################################################################
                pt1=img.shape[1] / 2
                pt2=img.shape[1] / 2 + DISTBETWEENPOINTS
                cv2.line(copy, (pt1, 0), (pt1, img.shape[0]), (255, 127, 0), 2)
                cv2.line(copy, (pt2, 0), (pt2, img.shape[0]), (255, 127, 0), 2)
                ######################################################################################################################################




            else:
                # HardCoded Points
                ##################################################################################################################################
                # pt2 = img.shape[0] / 2 - 50  # Swapped pt1 and pt2 positons not tested
                # pt1 = img.shape[0] / 2
                # cv2.line(copy, (0, pt1), (img.shape[1], pt1), (255, 127, 0), 2)
                # cv2.line(copy, (0,pt2), (img.shape[1], pt2), (255, 127, 0), 2)
                ##################################################################################################################################

                # Using DISTBETWEENPOINTS variable
                ########################################################################################################################################
                pt2 = img.shape[0] / 2 - DISTBETWEENPOINTS      # Swapped pt1 and pt2 positons not tested
                pt1 = img.shape[0] / 2
                cv2.line(copy, (0, pt1), (img.shape[1], pt1), (255, 127, 0), 2)
                cv2.line(copy, (0, pt2), (img.shape[1], pt2), (255, 127, 0), 2)
                ######################################################################################################################################

            # Preprocessing the Video
            ############################################################################################################
            imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imggray=cv2.GaussianBlur(imggray,(5,5),0)
            backsubimg = bgsubtractor.apply(imggray, None, 0.01)
            # cv2.imshow("BGSubImg",backsubimg)
            dilate = backsubimg

            for i in range(9):
                dilate = cv2.erode(dilate, None, iterations=1)
                dilate = cv2.dilate(dilate, None, iterations=2)

            dilate = cv2.dilate(dilate, None, iterations=1)
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
                cv2.rectangle(copy,(x,y),(x+w,y+h),(255,0,0),2)
                M = cv2.moments(c)
                if M["m00"] != 0:                       #Fixed Divide By Zero Error
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                else:
                    cx, cy = 0, 0
                #print(cx,xofline)

                if flagtostartlogic:
                    if LINE_ORIENTATION=="Vertical Reference Line":
                        if cx >= pt1 and cx <= pt1 + 10:
                            fc1=Framecount
                            # e=time.time()
                            # print("E",e)
                            count = count + 1
                            print "Total Count",count
                            totalcounter.setText(str(count))
                            print "Countour Area", cv2.contourArea(c)
                            if cv2.contourArea(c)>=MWR1 and cv2.contourArea(c)<=MWR2:
                                mediumweigthcount = mediumweigthcount + 1
                                print "Medium Weighted Vehicle ",mediumweigthcount
                                mediumcounter.setText(str(mediumweigthcount))
                                detectedVehicle = "Medium Weighted Vehicle"


                            else:
                                heavyweigthcount = heavyweigthcount + 1
                                print "Heavy Weighted Vehicle ", heavyweigthcount
                                heavycounter.setText(str(heavyweigthcount))
                                detectedVehicle = "Heavy Weighted Vehicle"

                            if(RRM == detectedVehicle):
                                text = alertholder.text()
                                alertholder.setText(text + "\n Restricted Vehicle type found on Road")
                                detectedVehicle = "N/A"
                            else:
                                detectedVehicle = "N/A"


                        if cx>=pt2 and cx<pt2+10:
                            fc2=Framecount
                            numframe=fc2 - fc1
                            # print("NumberofFrames",numframe)
                            try:
                                t=numframe/fps
                            except ZeroDivisionError:
                                continue
                            # print("t",t)
                            # print("coincide")
                            # s=time.time()
                            # print("S", s)
                            # y=s-e
                            # print("Y",y)
                            try:
                                speed=round((0.02*3600/t)%100,2)
                                # speed = 2*1000/(numframe*fps)
                                # speed = abs(speed)
                                # # speed = '{:.2f}'.format(speed).replace('.', '')

                            except :
                                continue
                            print speed,"km/h"
                            if(speed>SPEED_LIMIT):
                                name = "Snaps\\"+"ID"+str(count)+" "+str(speed)+" "+"kmph"+".jpg"
                                # crop_img = img[int(y):int(y+w+100),int(x):int(x+h+100)]
                                crop_img = img[int(y):int(y + w ), int(x):int(x + h )]
                                cv2.imwrite(name,crop_img)
                                text =alertholder.text()
                                alertholder.setText(text+"\n Speed limit crossed")


                            # # imagefornumberplate
                            # if cx==img.shape[1]/2:
                            #     snap = "NumberPlate\\"+"xyz"+".png"
                            #     crop_img = copy[int(y):int(y + w ), int(x):int(x + h)]
                            #     cv2.imwrite(name, crop_img)

                            fc2=0
                            fc1=0
                            numframe=0

                    else:
                        if cy>=pt1 and cy<=pt1+19:
                            fc1 = Framecount
                            # e = time.time()
                            count=count+1
                            print "Total Count",count
                            totalcounter.setText(str(count))
                            print "Countour Area", cv2.contourArea(c)

                            if cv2.contourArea(c)>=MWR1 and cv2.contourArea(c)<=MWR2:
                                mediumweigthcount = mediumweigthcount + 1
                                print "Medium Weighted Vehicle ",mediumweigthcount
                                mediumcounter.setText(str(mediumweigthcount))
                                detectedVehicle = "Medium Weighted Vehicle"

                            else:
                                heavyweigthcount = heavyweigthcount + 1
                                print "Heavy Weighted Vehicle ",heavyweigthcount
                                heavycounter.setText(str(heavyweigthcount))
                                detectedVehicle = "Heavy Weighted Vehicle"

                            if (RRM == detectedVehicle):
                                text = alertholder.text()
                                alertholder.setText(text + "\n Restricted Vehicle type found on Road")
                                detectedVehicle = "N/A"
                            else:
                                detectedVehicle = "N/A"


                        if cx>=pt2 and cx<pt2+20:
                            # print
                            fc2 = Framecount
                            numframe = fc2 - fc1
                            # print("NumberofFrames", numframe)
                            t = numframe / fps
                            # s=time.time()
                            # y=s-e
                            try:
                                speed = round((0.05 * 3600 / t)%100, 2)
                                # speed = 0.05/ (numframe * fps)
                            except ZeroDivisionError:
                                continue

                            print speed,"km/h"

                            if(speed>SPEED_LIMIT):
                                name = "Snaps\\"+"ID"+str(count)+" "+str(speed)+" "+"kmph"+".jpg"
                                # crop_img = img[int(y):int(y+w+100),int(x):int(x+h+100)]
                                crop_img = img[int(y):int(y + w ), int(x):int(x + h )]
                                cv2.imwrite(name,crop_img)
                                text = alertholder.text()
                                alertholder.setText(text + "\n Speed limit crossed")
                            fc2 = 0
                            fc1 = 0




            ############################################################################################################


             # Drawing Centroids
             ###########################################################################################################
                cv2.circle(copy, (cx, cy), 3, (255, 0, 255), -1)
                cv2.putText(copy,"Count: "+str(count)+"  Speed: "+ str(speed) + " kmph", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                            0.55, (0, 255, 0), 2)
                # copy=cv2.resize(copy,(420,276))
                # cv2.namedWindow("Detected Vehicles", cv2.cv.CV_WINDOW_AUTOSIZE)
                cv2.imshow("Detected Vehicles", copy)
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
            if k==ord('s'):
                flagtostartlogic = True
                count=0
                speed=0
            ############################################################################################################

        # If no next frame is available i.e ret is false
        ################################################################################################################
        else:
            print("Video Ended")
            email()
            break
        ###############################################################################################################

    ip.release()
    cv2.destroyAllWindows()



if __name__=='__main__':

    # Setting parameters global that are required to run
    global IPVIDEONAME, LINE_ORIENTATION, SPEED_LIMIT, MWR1, MWR2, DISTBETWEENPOINTS,RRM

    # Setting the defaults for the variables for console application
    ####################################################################################################################
    IPVIDEONAME = "video.avi"
    LINE_ORIENTATION="Vertical Reference Line"
    SPEED_LIMIT=10
    MWR1=500
    MWR2=5000
    DISTBETWEENPOINTS=50
    RRM = "Medium Weighted Vehicle"
    #####################################################################################################################


    #Setting the Counter Window
    ####################################################################################################################
    app = QApplication(sys.argv)
    global e
    e = QWidget()
    e.setWindowTitle('Monitored Results')
    e.setGeometry(700, 100, 300, 300)

    totalcountlabel = QLabel("Total Vehicles")
    totalcounter = QLabel("N/A")
    heavyweightlbl = QLabel("Total Heavy Weighted Vehicles")
    heavycounter = QLabel("N/A")
    mediumweightlbl = QLabel("Total Medium Weighted Vehicles")
    mediumcounter = QLabel("N/A")
    alertboxlbl = QLabel("Alert box")
    alertholder = QLabel()

    label_layout1 = QVBoxLayout()

    label_layout1.addWidget(totalcountlabel)
    label_layout1.addWidget(totalcounter)
    label_layout1.addWidget(heavyweightlbl)
    label_layout1.addWidget(heavycounter)
    label_layout1.addWidget(mediumweightlbl)
    label_layout1.addWidget(mediumcounter)
    label_layout1.addWidget(alertboxlbl)
    label_layout1.addWidget(alertholder)

    e.setLayout(label_layout1)
    e.show()

    ####################################################################################################################


    # Calling the main logic function
    srs()
    sys.exit(app.exec_())


    # Connection from GUI
def valueSetter(window,browsefile, referenceline, t1, t2, t3, t4, dropbox,t5,t6):

    #Setting parameters global that are required to run
    global IPVIDEONAME, LINE_ORIENTATION, SPEED_LIMIT, MWR1, MWR2, DISTBETWEENPOINTS,RRM

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
        RRM = str(dropbox)

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


        # Setting the Counter Window
        ####################################################################################################################
        app = QApplication(sys.argv)
        global e
        e = QWidget()
        e.setWindowTitle('Monitored Results')
        e.setGeometry(700, 100, 300, 300)

        totalcountlabel = QLabel("Total Vehicles")
        global totalcounter,heavycounter,mediumcounter,alertholder
        totalcounter = QLabel("N/A")
        heavyweightlbl = QLabel("Total Heavy Weighted Vehicles")
        heavycounter = QLabel("N/A")
        mediumweightlbl = QLabel("Total Medium Weighted Vehicles")
        mediumcounter = QLabel("N/A")
        alertboxlbl = QLabel("Alert box")
        alertholder = QLabel()

        label_layout1 = QVBoxLayout()

        label_layout1.addWidget(totalcountlabel)
        label_layout1.addWidget(totalcounter)
        label_layout1.addWidget(heavyweightlbl)
        label_layout1.addWidget(heavycounter)
        label_layout1.addWidget(mediumweightlbl)
        label_layout1.addWidget(mediumcounter)
        label_layout1.addWidget(alertboxlbl)
        label_layout1.addWidget(alertholder)

        e.setLayout(label_layout1)
        e.show()
        ####################################################################################################################

        srs()
        sys.exit(app.exec_())



# Make Changes in the clone image not the original One
# Formula for Speed rectify
#Make the markers as wide as possible


# video.avi MWR Range : 2000 to 5000
# video3.mp4 MWR Range : 500 to 25000
