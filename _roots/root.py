
#?PyQt6
from PyQt6.QtWidgets import QWidget,QMainWindow,QVBoxLayout,QApplication,QStackedWidget,QLineEdit
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction,QIcon

#? Miscellaneous
from pathlib import Path as pa
from functools import partial as pars
import sys as sy


#? custom
from HelperClass import HelperClass
from Events import AcceptUrlConnectEvents
from Queries import Queries

class MongoDbAssignment(QMainWindow):
    def __init__(self):
        super().__init__()
        self.directAttachments()
        self.initMainWin()

    def initMainWin(self):
        self.mainWindow()
        mWid = QWidget()
        mVLay = QVBoxLayout()
        MainStack = self.AcceptUrlNConnect(mVLay)
        self.FindHighest(MainStack)
        mWid.setLayout(mVLay)
        self.setCentralWidget(mWid)
        self.show()

    def directAttachments(self):
        self.rootFol = str(pa(__file__).parent.parent).replace("\\","/")
        self.dbPathToStudents = None
        self.connectedInfo = {
            "connected":False,
            "connected Url": None,
            "uploaded":False,
            "collectionExists": False,
            "client":None
        }
        self.loadingSpinner = HelperClass.graphicSpinner(self)

    def mainWindow(self):
        self.setWindowTitle("Assignment 2")
        self.setMinimumSize(QSize(400,500))
        self.setWindowIcon(QIcon(self.rootFol + "/data/calendar-assignment-icon_118813-1085.jpg"))
        cusMenu = self.menuBar()
        AppBox = cusMenu.addMenu("App")
        exitAction = QAction("Exit",self)
        exitAction.setShortcut("ctrl+e")
        exitAction.triggered.connect(pars(HelperClass.ExitFunc,self))
        AppBox.addAction(exitAction)

    def AcceptUrlNConnect(self,mVLay:QVBoxLayout):
        MainStWCon = QStackedWidget()
        MainStWCon.setMinimumHeight(150)
        widget1 = QWidget()
        vLay = QVBoxLayout(widget1)
        w1Des,warnLabel = HelperClass.HeadingNDes("Mongo Url","Enter your connection string that you got from your mongo db cluster (ex: mongodb+srv//...) .",180,400)
        vLay.addWidget(w1Des)  
        mongoStr = QLineEdit(self)
        mongoStr.setPlaceholderText("Enter your mongo url.")
        mongoStr.setFixedHeight(40)
        vLay.addWidget(mongoStr)
        ConnectBut = HelperClass.ProducePushBut(self,"Connect",AcceptUrlConnectEvents.connectDb,50,[self,mongoStr,MainStWCon,warnLabel])
        vLay.addWidget(ConnectBut)
        widget1.setLayout(vLay) 
        MainStWCon.addWidget(widget1)
        mVLay.addWidget(MainStWCon)
        return MainStWCon

    def FindHighest(self,mainStackWidget:QStackedWidget):
        """ Find the student name who scored maximum scores in all (exam, quiz and homework)? """
        widget = QWidget(self)
        vLay = QVBoxLayout(widget)
        desNHeading,_ = HelperClass.HeadingNDes("Find the student name who scored maximum scores in all (exam, quiz and homework)?","Query: db.collection.aggregate([{$sort:{scores.0.score:-1}},{$limit: 1}]) for exam, similar query for rest: changing index of array in the query of the rest. ",0,380,400,100)
        vLay.addWidget(desNHeading)
        
        mainStackWidget.addWidget(widget)
        but = HelperClass.ProducePushBut(self,"Highest",Queries.InDb1,30,[self,vLay])
        vLay.addWidget(but)
        widget.setLayout(vLay)





if not QApplication.instance():
    app = QApplication(sy.argv)
else:
    app = QApplication.instance()

mongo1 = MongoDbAssignment() 

sy.exit(app.exec())