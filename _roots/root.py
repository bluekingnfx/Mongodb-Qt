
#?PyQt6
from PyQt6.QtWidgets import QWidget,QMainWindow,QVBoxLayout,QApplication,QStackedWidget,QLineEdit,QScrollArea,QHBoxLayout
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction,QIcon

#? Miscellaneous
from pathlib import Path as pa
from functools import partial as pars
import sys as sy
import typing as ty


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
        self.FindBelowAvg(MainStack)
        self.AssignPassOrFail(MainStack)
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

        NavWidget = self.Nav(MainStWCon)

        ConnectBut = HelperClass.ProducePushBut("Connect",AcceptUrlConnectEvents.connectDb,50,[self,mongoStr,MainStWCon,NavWidget,widget1,warnLabel])
        vLay.addWidget(ConnectBut)
        widget1.setLayout(vLay) 
        MainStWCon.addWidget(widget1)
        mVLay.addWidget(MainStWCon)
        mVLay.addWidget(NavWidget)
        return MainStWCon

    def FindHighest(self,mainStackWidget:QStackedWidget):
        """ Find the student name who scored maximum scores in all (exam, quiz and homework)? """
        scrollArea = HelperClass.ProduceScrollArea()
        widget = QWidget()
        vLay = QVBoxLayout(widget)
        desNHeading,_ = HelperClass.HeadingNDes("1) Find the student name who scored maximum scores in all (exam, quiz and homework)?","Query: db.collection.aggregate([{$sort:{scores.0.score:-1}},{$limit: 1}]) for exam, similar query for rest: changing index of array in the query of the rest. ",0,380,400,100)
        vLay.addWidget(desNHeading)
    
        but = HelperClass.ProducePushBut("Highest",Queries.InDb1,30,[self,vLay,widget])
        vLay.addWidget(but)
        widget.setLayout(vLay)
        widget.setMaximumWidth(450)
        scrollArea.setWidget(widget)
        mainStackWidget.addWidget(scrollArea)

    def Nav(self,MStackWidget:QStackedWidget) -> QWidget:
        def navCore(_,typeBut:ty.Union[ty.Literal["prev"],ty.Literal["next"]]):
            if(typeBut == "prev"):
                MStackWidget.setCurrentIndex(MStackWidget.currentIndex() - 1)
            else:
                MStackWidget.setCurrentIndex(MStackWidget.currentIndex() + 1)
        widget = QWidget()
        butLay = QHBoxLayout()
        prevBut = HelperClass.ProducePushBut("Previous",navCore,30,["prev"])
        nextBut = HelperClass.ProducePushBut("Next",navCore,30,["next"])
        butLay.addWidget(prevBut)
        butLay.addWidget(nextBut)
        widget.setLayout(butLay)
        widget.setHidden(True)
        return widget

    def FindBelowAvg(self,MainStackWidget:QStackedWidget):
        """ Find students who scored below average in the exam and pass mark is 40%? """
        scrollArea = HelperClass.ProduceScrollArea()
        widget = QWidget()
        vLay = QVBoxLayout(widget)
        desNHeading,_ = HelperClass.HeadingNDes("2) Find students who scored below average in the exam and pass mark is 40%?","Query: db.collection.aggregate([{'$match':{scores.0.'score':{'$lt':40}}},{'$project':{'_id':0,'name':1,'exam':{'$arrayElem':['$scores',1]}}},{'$set':{'exam':'exam.score'},{$sort:{'exam':-1}}]). Atomic operators other than $match used for optimization.",350,380,400,100)
        but = HelperClass.ProducePushBut("Below Average",Queries.InDb2,30,[self,vLay,widget])
        vLay.addWidget(desNHeading)
        vLay.addWidget(but)
        widget.setMaximumWidth(410)
        scrollArea.setWidget(widget)
        MainStackWidget.addWidget(scrollArea)

    def AssignPassOrFail(self,mainStackWidget:QStackedWidget):
        """
            ?Find students who scored below pass mark and assigned them as fail, and above pass mark as pass in all the categories. 
        """
        scrollArea = HelperClass.ProduceScrollArea()
        widget = QWidget()
        vLay = QVBoxLayout(widget)
        desNHeading,_ = HelperClass.HeadingNDes("3) Find students who scored below pass mark and assigned them as fail, and above pass mark as pass in all the categories.","Query:db.collection.updateMany({},{'$set':{'scores.$[elem].grade':'pass'}},{'arrayFilters':[{'elem.score':{$lt:40}}]}) for fail, similarly $set fail for $gte:pass",0,380,380,200)
        vLay.addWidget(desNHeading)

        butContainer = QWidget()
        HLayBut = QHBoxLayout()
        butToFetch = HelperClass.ProducePushBut("Fetch document",AcceptUrlConnectEvents.fetchSampleDoc,30,[self,vLay])
        but = HelperClass.ProducePushBut("Assign status",Queries.InDb3,30,[self,butToFetch])
        HLayBut.addWidget(but)
        HLayBut.addWidget(butToFetch)
        butContainer.setLayout(HLayBut)
        butContainer.setFixedWidth(400)

        vLay.addWidget(butContainer)
        widget.setLayout(vLay)
        widget.setMaximumWidth(450)
        scrollArea.setWidget(widget)
        mainStackWidget.addWidget(scrollArea)

    





if not QApplication.instance():
    app = QApplication(sy.argv)
else:
    app = QApplication.instance()

mongo1 = MongoDbAssignment() 

sy.exit(app.exec())