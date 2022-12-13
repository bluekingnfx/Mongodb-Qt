from PyQt6.QtWidgets import QMessageBox

import json as Js
import typing as ty

from HelperClass import HelperClass 

class DatabaseConnection():
    @classmethod
    def createAndUploadTheFile(cls,client,path,self,connectedInfo:dict,parent:QMessageBox):
        
        def creatingDb(classroom):
            students = classroom.students

            try:
                with open(path,"r") as f:
                    data = Js.loads(f.read())
                    
                    students.insert_many(data)
                    HelperClass.ProduceMessageBox(self,"about","Successful","Inserted all the records in the database")
                    self.connectedInfo = {
                        **connectedInfo,
                        "collectionExists":False,
                        "uploaded":True,
                    }
                    
            except Exception as e:
                HelperClass.ProduceMessageBox(self,'about',"Error!","Unable to upload documents. Possible fixes: Turn on internet connection, or force reupload.")
                print(e)
        classroom = client.classroom
        creatingDb(classroom)

if __name__ == "__main__":
    DatabaseConnection()