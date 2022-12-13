
from pymongo import collection

from PyQt6.QtWidgets import QPushButton,QVBoxLayout,QGroupBox

from HelperClass import HelperClass



class Queries():

    @classmethod
    def InDb1(cls,but:QPushButton,selfMain,VLay:QVBoxLayout):
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

            HelperClass.setButDisabled("Processed.",but)
            highestGroup = QGroupBox()
            

        except Exception as e:
            print(e)




