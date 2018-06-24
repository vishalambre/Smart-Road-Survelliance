import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#Other Imports
from BackendScript import  valueSetter
from Graph import *

def main():
    app = QApplication(sys.argv)
    global w
    w = QWidget()
    w.setWindowTitle('Smart Road Survelliance')
    w.setGeometry(100,100,500,300)
    # w.resize(500,500)

    #LABELS
    global browsefile,countlabelvalue
    browsefile = QLabel('No file selected')
    browsefile.setAlignment(Qt.AlignCenter)
    vehicleCountinglbl = QLabel("Vehicle Counting")
    vehicleClassificationlbl=QLabel("Vehicle Classification")
    MWRlbl = QLabel("Medium Weighted Range")
    HWRlbl = QLabel("Heavy Weighted Range")
    RRMlbl = QLabel("Resticted Road Monitoring")
    distancebetweenpts=QLabel("Known distance between two points")
    SLVlbl = QLabel("Speed Limit Violation")
    SLlbl = QLabel("Speed Limit")
    toLabel1 = QLabel("TO")
    toLabel1.setAlignment(Qt.AlignCenter)
    toLabel2 = QLabel("TO")
    toLabel2.setAlignment(Qt.AlignCenter)
    # countlabelvalue=QLabel("0");


    # RadioButtons
    global hrefline,vrefline
    hrefline = QRadioButton("Horizontal Reference Line")
    hrefline.setIcon(QIcon("hor_line"))
    vrefline = QRadioButton("Vertical Reference Line")
    vrefline.setIcon(QIcon("ver_line.png"))

    #TextFields
    global t1,t2,t3,t4,t5,t6
    t1 = QLineEdit()
    t1.setMaxLength(4)
    # t1.setAlignment(Qt.AlignRight)

    t2 = QLineEdit()
    t2.setMaxLength(4)
    # t2.setAlignment(Qt.AlignRight)

    t3 = QLineEdit()
    t3.setMaxLength(4)
    # t3.setAlignment(Qt.AlignRight)

    t4 = QLineEdit()
    t4.setMaxLength(4)
    # t4.setAlignment(Qt.AlignRight)

    t5=QLineEdit()

    t6=QLineEdit()
    t6.setMaxLength(3)

    # Dropbox
    global dropbox
    dropbox = QComboBox()
    dropbox.addItem("Heavy Weighted Vehicle")
    dropbox.addItem("Medium Weighted Vehicle")
    # dropbox.addItem("Light Weighted")

    # ButtonField
    browsebtn = QPushButton("Browse")
    browsebtn.clicked.connect(getfiles)
    webcambtn = QPushButton("Webcam")
    webcambtn.clicked.connect(setWebCam)
    startbtn = QPushButton("Start!")
    startbtn.clicked.connect(start)
    # plotGraph = QPushButton("Plot Graph")
    # plotGraph.clicked.connect(graph)




    # Layouts
    label_layout = QVBoxLayout()
    
    # element_layout = QHBoxLayout()
    label_layout.addWidget(browsefile)
    label_layout.addWidget(browsebtn)
    label_layout.addWidget(webcambtn)
    label_layout.addWidget(vehicleCountinglbl)
    label_layout.addWidget(hrefline)
    label_layout.addWidget(vrefline)
    label_layout.addWidget(vehicleClassificationlbl)
    label_layout.addWidget(MWRlbl)
    label_layout.addWidget(t1)
    label_layout.addWidget(toLabel1)
    label_layout.addWidget(t2)
    label_layout.addWidget(HWRlbl)
    label_layout.addWidget(t3)
    label_layout.addWidget(toLabel2)
    label_layout.addWidget(t4)
    label_layout.addWidget(RRMlbl)
    label_layout.addWidget(dropbox)
    label_layout.addWidget(distancebetweenpts)
    label_layout.addWidget(t5)
    label_layout.addWidget(SLVlbl)
    label_layout.addWidget(SLlbl)
    label_layout.addWidget(t6)
    label_layout.addWidget(startbtn)
    # label_layout.addWidget(countlabelvalue)
    # label_layout.addWidget(plotGraph)

    w.setLayout(label_layout)

    w.show()

    sys.exit(app.exec_())


def start():
    print("Btn Clicked")

    if(hrefline.isChecked()):
        valueSetter(w, browsefile.text(), hrefline.text(), t1.text(), t2.text(), t3.text(), t4.text(), dropbox.currentText(), t5.text(), t6.text())
    else:
        valueSetter(w, browsefile.text(), vrefline.text(), t1.text(), t2.text(), t3.text(), t4.text(), dropbox.currentText(), t5.text(),t6.text())


def getfiles():
    fname = QFileDialog.getOpenFileName( w,'Open file')
    if fname:
        browsefile.setText(fname)
    else:
        browsefile.setText('No file selected')

def setWebCam():
    browsefile.setText("WebCam Selected")

if __name__ == '__main__':
    main()




