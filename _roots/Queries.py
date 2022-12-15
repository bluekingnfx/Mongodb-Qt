
from PyQt6.QtWidgets import QPushButton,QVBoxLayout,QGroupBox,QFrame,QWidget,QTableWidget,QTableWidgetItem,QHBoxLayout


from pymongo import collection
from time import time as t


from HelperClass import HelperClass
from Events import AcceptUrlConnectEvents as AUC



class Queries():

    @classmethod
    def showError(cls,MainSelf,CodeError,but:QPushButton,butText:str):
        if CodeError == None:
            HelperClass.ProduceMessageBox(MainSelf,"about","Error!","Enable to complete the operation. Possible fixed: Check the connection, Problem persists try to exits the app or clear the database and recreate it.")
        else:
            HelperClass.ProduceMessageBox(MainSelf,"about","Error!",f"Enable to complete the operation. Possible fixed: Check the connection, Problem persists try to exits the app or clear the database and recreate it.Code Error:{CodeError}")
        HelperClass.setButEnabled(butText,but)

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
            try:
                err = str(e)
                cls.showError(selfMain,e,but,"Highest")
            except:
                cls.showError(selfMain,None,but,"Highest")

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
            rows = res.__len__()+1
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
            try:
                err = str(e)
                cls.showError(selfMain,e,but,"Below Average")
            except:
                cls.showError(selfMain,None,but,"Below Average")
        
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

        except Exception as e:
            try:
                err = str(e)
                cls.showError(selfMain,e,but,"Assign status")
            except:
                cls.showError(selfMain,None,but,"Assign status")
        
    @classmethod
    def InDb4(cls,but:QPushButton,selfMain,MainVLay:QVBoxLayout):
        HelperClass.setButDisabled("Loading...",but)
        try:
            coll:collection.Collection = selfMain.dbPathToStudents
            outColl = f"summary{str(int(t()))}"
            pipeline = [
                {
                    "$project":{
                        "_id":0,
                        "exam":{
                            "$arrayElemAt":["$scores",0]
                        },
                        "quiz":{
                            "$arrayElemAt":["$scores",1]
                        },
                        "homework":{
                            "$arrayElemAt":["$scores",2]
                        }
                    }
                },{
                    "$group":{
                        "_id":0,
                        "examTotal":{"$sum":"$exam.score"},
                        "examAvg":{"$avg":"$exam.score"},
                        "quizTotal":{"$sum":"$quiz.score"},
                        "quizAvg":{"$avg":"$quiz.score"},
                        "homeworkTotal":{"$sum":"$homework.score"},
                        "homeworkAvg":{"$avg":"$homework.score"}
                    }
                },
                {
                    "$out":outColl
                }
            ]
            coll.aggregate(pipeline)
            widgetLoc = QWidget()
            vLayLoc = QVBoxLayout()
            label, = HelperClass.produceLabels([
                ("text",f"Collection named {outColl} was created with one document containing the summary. Click Retrieve to retrieve the doc.","font-size:16px;")
            ])
            but1 = HelperClass.ProducePushBut("Retrieve",AUC.fetchSampleDoc,30,[selfMain,vLayLoc,selfMain.classRoomPath[outColl],0,350])
            vLayLoc.addWidget(label)
            vLayLoc.addWidget(but1)
            widgetLoc.setLayout(vLayLoc)
            MainVLay.addWidget(widgetLoc)
            HelperClass.setButEnabled("Processed.",but)
            
        except Exception as e:
            try:
                err = str(e)
                cls.showError(selfMain,e,but,"Create Summary Collection")
            except:
                cls.showError(selfMain,None,but,"Create Summary Collection")

    @classmethod
    def InDb5(cls,but:QPushButton,selfMain,MainVLay:QVBoxLayout):

        def ProduceTable(labelText,arr):
            label, = HelperClass.produceLabels([
                ("text",labelText,"font-size:16px")
            ],None,True,200)
            rows1 = arr.__len__()+1
            columns1 = 2
            table = QTableWidget(rows1,columns1)
            table.setItem(0,0,QTableWidgetItem("Name"))
            table.setItem(0,1,QTableWidgetItem("Average"))
            table.setColumnWidth(0,140)
            table.setColumnWidth(1,200)
            HelperClass.FillTable(table,arr,0,"name",1)
            HelperClass.FillTable(table,arr,1,"averageCombined",1)
            MainVLay.addWidget(label)
            MainVLay.addWidget(table)


        HelperClass.setButDisabled("Loading...",but)
        coll:collection.Collection = selfMain.dbPathToStudents
        outColl1 = f"PassedByAverageAllCatagories{str(int(t()))}"
        outColl2 = f"FailedByAverageAllCatagories{str(int(t()))}"
        pipeline1 = [
            {
                "$set":{
                    "averageCombined":{
                        "$reduce":{
                            "input":"$scores",
                            "initialValue":0,
                            "in":{"$add":["$$value","$$this.score"]}
                        }
                    }
                }
            },
            {
                "$set":{
                    "averageCombined":{
                        "$divide":["$averageCombined",3]
                    }
                }
            },
            {
                "$match":{
                    "averageCombined":{
                        "$gte":40
                    }
                }
            },
            {
                "$out":outColl1
            }
        ]
        pipeline2 = [
            {
                "$set":{
                    "averageCombined":{
                        "$reduce":{
                            "input":"$scores",
                            "initialValue":0,
                            "in":{"$add":["$$value","$$this.score"]}
                        }
                    }
                }
            },
            {
                "$set":{
                    "averageCombined":{
                        "$divide":["$averageCombined",3]
                    }
                }
            },
            {
                "$match":{
                    "averageCombined":{
                        "$lt":40
                    }
                }
            },
            {
                "$out":outColl2
            }
        ]
        try:
            coll.aggregate(pipeline1)
            coll.aggregate(pipeline2)
            res1Coll:collection.Collection = selfMain.classRoomPath[outColl1]
            res2Coll:collection.Collection = selfMain.classRoomPath[outColl2]
            res1 = list(res1Coll.find({},{"name":1,"_id":0,"averageCombined":1}))
            res2 = list(res2Coll.find({},{"name":1,"_id":0,"averageCombined":1}))
            ProduceTable("Following table represents all the students who got above average of combined catagories, indeed makes them PASS.",res1)
            ProduceTable("Following table represents all the students who got below average of combined catagories, indeed makes them FAIL.",res2)
            HelperClass.setButEnabled("Processed.",but)

        except Exception as e:
            try:
                err = str(e)
                cls.showError(selfMain,e,but,"Create Collection for below and above average.")
            except:
                cls.showError(selfMain,None,but,"Create Collection for below and above average.")

    @classmethod
    def InDb6(cls,but:QPushButton,selfMain,MainVLay:QVBoxLayout,widget:QWidget):
        outColl = f"FailedAll{str(int(t()))}"
        def PullColl(but):

            try:
                coll = selfMain.classRoomPath[outColl]
                res = list(coll.find({}))
                rows = res.__len__()+1
                columns = 4
                table = QTableWidget(rows,columns)
                table.setItem(0,0,QTableWidgetItem("Name"))
                table.setItem(0,1,QTableWidgetItem("Exam"))
                table.setItem(0,2,QTableWidgetItem("Quiz"))
                table.setItem(0,3,QTableWidgetItem("HomeWork"))
                table.setColumnWidth(0,140)
                table.setColumnWidth(1,150)
                table.setColumnWidth(2,150)
                table.setColumnWidth(3,150)
                HelperClass.FillTable(table,res,0,"name",1)
                HelperClass.FillTable(table,res,1,"exam",1)
                HelperClass.FillTable(table,res,2,"quiz",1)
                HelperClass.FillTable(table,res,3,"homework",1)
                MainVLay.addWidget(table)
            except Exception as E:
                print(E)

        HelperClass.setButDisabled("Loading...",but)
        pipeline = [
            {
                "$match":{
                    "$and":[
                        {"scores.0.score":{"$lt":40}},
                        {"scores.1.score":{"$lt":40}},
                        {"scores.2.score":{"$lt":40}}
                    ]
                }
            },
            {
                "$project":{
                    "_id":0,
                    "exam":{
                        "$arrayElemAt":["$scores",0]
                    },
                    "quiz":{
                        "$arrayElemAt":["$scores",1]
                    },
                    "homework":{
                        "$arrayElemAt":["$scores",2]
                    },
                    "name":1
                }
            },{
                "$set":{
                    "exam":"$exam.score",
                    "quiz":"$quiz.score",
                    "homework":"$homework.score"
                }
            },
            {
                "$out":outColl
            }
        ]

        try:
            coll:collection.Collection = selfMain.dbPathToStudents
            coll.aggregate(pipeline)
            widgetLoc = QWidget()
            vLayLoc = QVBoxLayout()
            label, = HelperClass.produceLabels([
                ("text",f"Collection named {outColl} was created with documents containing people who failed in all catagories. Click Retrieve to retrieve the doc.","font-size:16px;")
            ])
            but1 = HelperClass.ProducePushBut("Retrieve",PullColl,30)
            vLayLoc.addWidget(label)
            vLayLoc.addWidget(but1)
            widgetLoc.setLayout(vLayLoc)
            MainVLay.addWidget(widgetLoc)
            HelperClass.setButEnabled("Processed.",but)

        except Exception as e:
            try:
                err = str(e)
                cls.showError(selfMain,e,but,"Create Failed all")
            except:
                cls.showError(selfMain,None,but,"Create Failed all")
        
    @classmethod
    def InDb7(cls,but:QPushButton,selfMain,MainVLay:QVBoxLayout,widget:QWidget):
        outColl = f"PassedAll{str(int(t()))}"
        def PullColl(but):

            try:
                coll = selfMain.classRoomPath[outColl]
                res = list(coll.find({}))
                rows = res.__len__()+1
                columns = 4
                table = QTableWidget(rows,columns)
                table.setItem(0,0,QTableWidgetItem("Name"))
                table.setItem(0,1,QTableWidgetItem("Exam"))
                table.setItem(0,2,QTableWidgetItem("Quiz"))
                table.setItem(0,3,QTableWidgetItem("HomeWork"))
                table.setColumnWidth(0,140)
                table.setColumnWidth(1,150)
                table.setColumnWidth(2,150)
                table.setColumnWidth(3,150)
                HelperClass.FillTable(table,res,0,"name",1)
                HelperClass.FillTable(table,res,1,"exam",1)
                HelperClass.FillTable(table,res,2,"quiz",1)
                HelperClass.FillTable(table,res,3,"homework",1)
                widget.setMinimumHeight(800)
                MainVLay.addWidget(table)
            except Exception as E:
                print(E)
        HelperClass.setButDisabled("Loading...",but)
        pipeline = [
            {
                "$match":{
                    "$and":[
                        {"scores.0.score":{"$gte":40}},
                        {"scores.1.score":{"$gte":40}},
                        {"scores.2.score":{"$gte":40}}
                    ]
                }
            },
            {
                "$project":{
                    "_id":0,
                    "exam":{
                        "$arrayElemAt":["$scores",0]
                    },
                    "quiz":{
                        "$arrayElemAt":["$scores",1]
                    },
                    "homework":{
                        "$arrayElemAt":["$scores",2]
                    },
                    "name":1
                }
            },{
                "$set":{
                    "exam":"$exam.score",
                    "quiz":"$quiz.score",
                    "homework":"$homework.score"
                }
            },
            {
                "$out":outColl
            }
        ]

        try:
            coll:collection.Collection = selfMain.dbPathToStudents
            coll.aggregate(pipeline)
            widgetLoc = QWidget()
            vLayLoc = QVBoxLayout()
            label, = HelperClass.produceLabels([
                ("text",f"Collection named {outColl} was created with documents containing people who passed in all catagories. Click Retrieve to retrieve the doc.","font-size:16px;")
            ])
            but1 = HelperClass.ProducePushBut("Retrieve",PullColl,30)
            vLayLoc.addWidget(label)
            vLayLoc.addWidget(but1)
            widgetLoc.setLayout(vLayLoc)
            MainVLay.addWidget(widgetLoc)
            HelperClass.setButEnabled("Processed.",but)

        except Exception as e:
            try:
                err = str(e)
                cls.showError(selfMain,e,but,"Create Passed all")
            except:
                cls.showError(selfMain,None,but,"Create Passed all")
        
