# MongoDB problem statement GUI Solution.

## To Get Started

### Python > 3.5 is a recommended.
Install typing module to avoid run time failures if you are below 3.5.

### Altering the source code. Steps as follows.
1) Open the command prompt or the shell depending upon your os.
2) Copy and run the following command ``pip install -r requirements.txt`` from MongoDb-Qt as root folder in the shell or cmd.
3) If it is not successfully installed run ``pip install pymongo PyQt6``.
4) Once installed, you need to run the **_roots/root.py** has it is the main file where Qt application starts.
5) You should potentially see a GUI, follow the instructions as per GUI. Process will be explained below.
6) You could freely mess around code and have fun.
7) If there is any issue, please PR.

### Installing via dist zip folder (Recommended).
1) Extract the zip `dist.zip` folder by Winzip or 7zip; any extraction software.
2) Once extracted open the exe file ``/dist/root/MongoDB Assignment.exe``. 
3) You are now in Python GUI.
4) Also given `root.spec` in the pulled code, if you familiar with `pyinstaller` which can be installed by `pip install pyinstaller` .After installation, you could rebuild the dist directory by running `pyinstaller root.spec`

### Introduction. 
The app is made to solve the problem statement from the file `Problem Statement.pdf` using python mongo framework and GUI Python Qt framework.

### Workings of the code.

#### Home window

![Screenshot1](/readMeImages/Screenshot1.jpg)


- In Home window, you need to enter a cluster url of the atlas client.
- Once entered, Click connect - There will prompt appear as in the following image.

![ScreenShot2](/readMeImages/Screenshot 2.jpg)

- ***Make sure connected database does not have classroom collection, unless the classroom collection is created by the app. There will be problem of overwriting, I am not responsible for any collection drop, no liabilities upon me cause I warned you, now.***

- Once you pressed ok, there will be prompt notifying you **Inserted the documents**. 
- Now again, click connect you will be moved to new gui with navigation buttons like the following image.

![Screenshot3](/readMeImages/Screenshot3.jpg)

- The Bold font describes the question from Problem statement Pdf.
- Next, Lesser contrast to previous describes the query that will be performed. **All the queries with explanation will be given in Queries and Elaboration section**.
- Clicking highest resolves to solution by performing query internally (3).
- There will be 7 question, you can navigate through and fetch documents by clicking the button which was described above(3).

### Folder structure and its contents.
1) ``dist`` : Contains the executable of the app.
2) ``roots/data`` : Contains the *students.json* from problem statement.pdf and app icon.
3) ``roots/DataBaseConnClass`` : Contains code for uploading the json into db. 
4) ``roots/Events``: Major connection Events.
5) ``roots/HelperClass``: Contains the Qt widget code to increase reusability.
6) ``roots/Queries`` : Core. Contains all the problem statements questions (1-7)


### Queries And Elaboration
1) Find the student name who scored maximum scores in all (exam, quiz and homework)?

```py
    #Query
    examHighest = list(coll.aggregate([ #! Aggregation Frame work.
        {
            "$sort":{ #!Sorting from Z-A (Descending order)
                "scores.0.score":-1
            }
        },{
            "$limit":1 #!Limiting to one document to use resource efficiently.
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

    #! Finally for loop to find the total marks of each elem 
    # in the scores array and adding it to get overall
    # out of 300.
```

2) Find students who scored below average in the exam and pass mark is 40%?
```py
    pipeline = [
        {
            "$match": { 
                #! This stage matches the 
                # documents whose first element of 
                # scores array is less than 40
                "scores.0.score": {
                    "$lt":40
                }
            }
        },{
            #! Using project stage as formatter.
            # including name, and formatting exam to the 
            # first elem of the scores field in the doc
            # Also achieved by $first atomic operator.
            "$project":{
                "name":1,
                "_id":0,
                "exam":{
                    "$arrayElemAt":["$scores",0]
                }
            }
        },{
            #! Setting the exam directed to exam from 
            # previous exam:{score:100,type:"exam"}
            "$set":{
                "exam":"$exam.score"
            }
        },{
            #! Sorting Descending.
            "$sort":{
                "exam":-1
            }
        }

        #! $project and $sort and $set
        # used to ease the returned data
        # for client side operation.
    ]
   ```

3) Find students who scored below pass mark and assigned them as fail, and above pass mark as pass in all the categories
   ```py
    #?For academically failed students
    coll.update_many({
        #! Empty first to go through all
    },{
        "$set":{
            "scores.$[elem].grade":"Fail" 
            #! Using positional operator 
            #! to assign Fail to each category 
            # based on array filters.
        }
    },array_filters=[{
        "elem.score":{
            "$lt":40  #! Array Filter applied to each elem to the array. 
            #Less than
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
            "$gte":40 #greater or equal to
        }
    }])

   ```

4) Find the total and average of the exam, quiz and homework and store them in a separate collection.
```py
     pipeline = [
        {
            "$project":{ 
                #!Project as formatter and 
                #! assigning eachElem of the scores array.
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
                #! Above grouping returns docs in shape
                #! {exam:{score:101,type:'exam'},
                # quiz:{score:102,type:'quiz'},
                # (...likewise for homework)},
                # {exam:{score:101,type:'exam'},
                # quiz:{score:102,type:'quiz'},
                # (...likewise for homework)}, so on..
                #! Grouping by Null results in one huge document. 
                # Indeed, helps in math operations like avg and sum.
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
            #! helps to write a new coll : outColl is a str along with type casted time.time() for unique collection name 
            "$out":outColl
        }
    ]
```

5) Create a new collection which consists of students who scored below average and above 40% in all the categories.
   ```py
        outColl1 = f"PassedByAverageAllCatagories{str(int(t()))}"
        outColl2 = f"FailedByAverageAllCatagories{str(int(t()))}"
    pipeline1 = [
        {
            "$set":{
                "averageCombined":{ 
                    "$reduce":{ #! reduce operator
                        "input":"$scores", #! array field
                        "initialValue":0, #! given the initial value
                        "in":{"$add":["$$value","$$this.score"]} #! in,property operates the initial 
                        #value and each Elem.

                    }
                }
            }
        },
        {
            "$set":{
                "averageCombined":{
                    "$divide":["$averageCombined",3] #Dividing by 3 to #! get average.
                }
            }
        },
        {
            "$match":{
                "averageCombined":{
                    "$gte":40 #2 find all docs 
                    # greater than or equal to 40.
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
                    "$lt":40 #! less than 40 docs will be returned.
                }
            }
        },
        {
            "$out":outColl2 #! creating collection.
        }
    ]
   ```

6) Create a new collection which consists of students who scored below the fail mark in all the categories.
   ```py
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
                "_id":0, #!explained above.
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
    ```

7) Create a new collection which consists of students who scored above pass mark in all the categories.
   
    ```py
        pipeline = [
            {
                "$match":{
                    "$and":[
                        {"scores.0.score":{"$gte":40}},
                        {"scores.1.score":{"$gte":40}}, #! Like above 60
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
    ```

### MADE WITH LOVE ❤️.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
