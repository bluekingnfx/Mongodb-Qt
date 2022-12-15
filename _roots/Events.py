from PyQt6.QtWidgets import QLabel,QLineEdit,QStackedWidget,QPushButton,QWidget,QVBoxLayout

from pymongo import MongoClient,collection
from random import randint
import json
import typing as ty

from HelperClass import HelperClass
from DataBaseConnClass import DatabaseConnection


class AcceptUrlConnectEvents():

    @classmethod
    def changeTheStackWidgetTo1Q(cls,MainStackW:QStackedWidget,but:QPushButton,NavWidget:QWidget,connectWid:QWidget):
        HelperClass.setButEnabled("Connect",but)
        MainStackW.setCurrentIndex((MainStackW.currentIndex())+1)
        MainStackW.removeWidget(connectWid)
        NavWidget.setHidden(False)

    @classmethod
    def connectDb(cls,but,self,edit:QLineEdit,MainStackW:QStackedWidget,NavWidget:QWidget,connectWid,warnLabel:QLabel):
        try:
            HelperClass.setButDisabled("Loading...",but)
            connectStr = edit.text()
            client = MongoClient(connectStr)
            
            if "classroom" in client.list_database_names():
                db = client.classroom
                self.classRoomPath = db
                if "students" in db.list_collection_names():
                    self.dbPathToStudents = db.students
                    self.connectedUrl = {
                        "connected":True,
                        "connected Url": connectStr,
                        "collectionExists":True,
                        "uploaded":False,
                        "client":client
                    }
                    HelperClass.ProduceMessageBox(self,"about","Connected","Mongo database has been connected. There is classroom database with students collection.",cls.changeTheStackWidgetTo1Q,None,[MainStackW,but,NavWidget,connectWid])


                else:
                    self.connectedInfo = {
                        "connected":True,
                        "connected Url": connectStr,
                        "collectionExists":False,
                        "uploaded":False,
                        "client":client 
                    }
                    raise Exception("No collection")    
            else: 
                self.connectedInfo = {
                    "connected":True,
                    "connected Url": connectStr,
                    "collectionExists":False,
                    "uploaded":False,
                    "client":client
                }
                raise Exception("No db")
        except Exception as e:
            if str(e) == "No db" or str(e) == "No collection":
                if str(e) == "No db":
                    title = "Connected but No database."
                    des = "There is no database named classroom in your atlas client. Press Ok, if you like to create a classroom database and students collection. Cancel if you are comfortable to, manually create database classroom and collection students, students.json must be added to students collection."
                else:
                    title = "Connected but No collection"
                    des = "Connected but there is no students collection. Press ok to automatically create the collection with records,or cancel, so you can manually create the collection in the database classroom and import students.json"
                
                HelperClass.ProduceMessageBox(self,"question",title,des,DatabaseConnection.createAndUploadTheFile,None,[self.connectedInfo["client"],self.rootFol+"_roots/data/students.json",self,self.connectedInfo],[],True)
            
            else:
                HelperClass.ProduceMessageBox(self,"about","Error","Unable to connect to the client. Possible fixes: Check the mongo url, see if the database is up.")
                print(e)
            HelperClass.setButEnabled("Connect",but)
        
    @classmethod
    def fetchSampleDoc(cls,but,selfMain,VLay:QVBoxLayout,collection = None, specificId:ty.Union[int,None] = None,heightOfLabel:int = 500):
        """
            specific id must be an integer, like _id:0, should not be objectId.
        """
        dBPath:collection.Collection
        if collection != None:
            dBPath = collection
            if specificId == None: raise Exception("No specific but collection is different.")
            no = specificId
        else:
            dBPath = selfMain.dbPathToStudents
            no = randint(1,200)
        
        try:
            item = dBPath.find_one({
                "_id":no
            })

            js = json.dumps(item,ensure_ascii=False,indent=4)
            label, = HelperClass.produceLabels([("text",js,"font-size:16px;border:1px solid #333;border-radius:4px")],None,True,heightOfLabel)
            label.setFixedWidth(300)
            VLay.addWidget(label)

        except Exception as E:
            try:
                err = str(E)
                HelperClass.ProduceMessageBox(selfMain,"about","Error!",f"Enable to complete the operation. Possible fixed: Check the connection, Problem persists try to exits the app or clear the database and recreate it. Code Error:{err}")
            except:
                HelperClass.ProduceMessageBox(selfMain,"about","Error!","Enable to complete the operation. Possible fixed: Check the connection, Problem persists try to exits the app or clear the database and recreate it.")
            
                