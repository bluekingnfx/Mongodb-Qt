
from pymongo import collection

from PyQt6.QtWidgets import QPushButton,QVBoxLayout,QGroupBox,QFrame,QWidget,QTableWidget,QTableWidgetItem

from HelperClass import HelperClass



class Queries():

    @classmethod
    def InDb1(cls,but:QPushButton,selfMain,VLay:QVBoxLayout,widget:QWidget):
        HelperClass.setButDisabled("Loading...",but)
        highest = []
        try:
            coll:collection.Collection = selfMain.dbPathToStudents
            examHighest = list(coll.aggregate([
                {
                    "$sort":{
                        "scores.0.score":-1
                    }
                },{
                    "$limit":1
                }
            ]))
            quizHighest = list(coll.aggregate([
                {
                    "$sort": {
                        "scores.1.score" : -1
                    }
                },{
                    "$limit":1
                }
            ]))
            homeWorkHighest = list(coll.aggregate([
                {
                    "$sort": {
                        "scores.2.score" : -1
                    }
                },{
                    "$limit":1
                }
            ]))

            people = [*examHighest,*quizHighest,*homeWorkHighest]
            for index,person in enumerate(people):
                averageArray = [i["score"] for i in person["scores"]]
                average = 0
                for i in averageArray:
                    average = average + i
                scoreNav = person["scores"][index]
                highest = [*highest,{
                    "name":person["name"],
                    "score":scoreNav["score"],
                    "type":scoreNav["type"],
                    "average":average
                }]

            HelperClass.setButEnabled("Processed.",but)
            highestGroup = QGroupBox("Highest in each subject.")
            vLayL = QVBoxLayout()
            labels = HelperClass.produceLabels([
                ("text",f"{i['name']} scored {i['score']} which is the maximum marks in {i['type']}.","font-size:16px") for i in highest
            ])

            for i in labels:
                vLayL.addWidget(i)
            
            frame = QFrame()
            frame.setFixedHeight(150)
            frame.setFrameShadow(frame.Shadow.Raised)
            frame.setFrameShape(frame.Shape.Box)
            frameVLay = QVBoxLayout()
            average = 0
            name = ""

            for i in highest:
                if(average < i["average"]):
                    average = i["average"]
                    name = i["name"]

            overallLabel, = HelperClass.produceLabels([
                ("text",f"Overall {name} scored maximum marks {average} of 300 in the entire class.","font-size: 18px; font-weight:500;")
            ],None,True,70)

            frameVLay.addWidget(overallLabel)
            frame.setFixedHeight(80)
            frame.setLayout(frameVLay)
            highestGroup.setLayout(vLayL)
            widget.setFixedWidth(410)
            VLay.addWidget(highestGroup)
            VLay.addWidget(frame)
            
            

        except Exception as e:
            print(e)

    @classmethod
    def InDb2(cls,but:QPushButton,selfMain,VLay:QVBoxLayout,widget:QWidget):
        HelperClass.setButDisabled("Loading...",but)
        pipeline = [{
            "$match": {
                "scores.0.score": {
                    "$lt":40
                }
            }
        },{
            "$project":{
                "name":1,
                "_id":0,
                "exam":{
                    "$arrayElemAt":["$scores",0]
                }
            }
        },{
            "$set":{
                "exam":"$exam.score"
            }
        },{
            "$sort":{
                "exam":-1
            }
        }]

        try:
            coll:collection.Collection = selfMain.dbPathToStudents
            res = list(coll.aggregate(pipeline))
            rows = res.__len__()
            columns = 2
            table = QTableWidget(rows,columns)
            widget.setFixedWidth(410)
            
            table.setItem(0,0,QTableWidgetItem("Name"))
            table.setItem(0,1,QTableWidgetItem("Marks"))
            table.setColumnWidth(0,140)
            table.setColumnWidth(1,200)
            HelperClass.FillTable(table,res,0,"name",1)
            HelperClass.FillTable(table,res,1,"exam",1)
            VLay.addWidget(table)
            HelperClass.setButEnabled("Processed",but)

        except Exception as e:
            print(e)
        
    @classmethod
    def InDb3(cls,but:QPushButton,selfMain,butToF:QPushButton):
        
        HelperClass.setButDisabled("Loading...",but)
        try:
            coll:collection.Collection = selfMain.dbPathToStudents

            #?For academically failed students
            coll.update_many({

            },{
                "$set":{
                    "scores.$[elem].grade":"Fail"
                }
            },array_filters=[{
                "elem.score":{
                    "$lt":40
                }
            }])

            #?Passed
            coll.update_many({

            },{
                "$set":{
                    "scores.$[elem].grade":"Pass"
                }
            },array_filters=[{
                "elem.score":{
                    "$gte":40
                }
            }])

            HelperClass.setButEnabled("Processed.",but)
            HelperClass.setButEnabled("Fetch Sample doc.",butToF)

        except Exception as E:
            print(E)
        
    @classmethod
    def InDb4():
        pass


