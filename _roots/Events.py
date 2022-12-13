from PyQt6.QtWidgets import QLabel,QLineEdit,QStackedWidget,QPushButton

from pymongo import MongoClient


from HelperClass import HelperClass
from DataBaseConnClass import DatabaseConnection


class AcceptUrlConnectEvents():

    @classmethod
    def changeTheStackWidgetTo1Q(cls,MainStackW:QStackedWidget,but:QPushButton):
        HelperClass.setButEnabled("Connect",but)
        MainStackW.setCurrentIndex((MainStackW.currentIndex())+1)

    @classmethod
    def connectDb(cls,but,self,edit:QLineEdit,MainStackW:QStackedWidget,warnLabel:QLabel):
            try:
                HelperClass.setButDisabled("Loading...",but)
                connectStr = edit.text()
                client = MongoClient(connectStr)
                if "classroom" in client.list_database_names():
                    db = client.classroom
                    if "students" in db.list_collection_names():
                        self.dbPathToStudents = db.students
                        self.connectedUrl = {
                            "connected":True,
                            "connected Url": connectStr,
                            "collectionExists":True,
                            "uploaded":False,
                            "client":client
                        }
                        HelperClass.ProduceMessageBox(self,"about","Connected","Mongo database has been connected. There is classroom database with students collection.",cls.changeTheStackWidgetTo1Q,None,[MainStackW,but])


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
                    
                    HelperClass.ProduceMessageBox(self,"question",title,des,DatabaseConnection.createAndUploadTheFile,None,[self.connectedInfo["client"],self.rootFol+"/data/students.json",self,self.connectedInfo],[],True)
                
                else:
                    HelperClass.ProduceMessageBox(self,"about","Error","Unable to connect to the client. Possible fixes: Check the mongo url, see if the database is up.")
                    print(e)
                HelperClass.setButEnabled("Connect",but)
                