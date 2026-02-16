class User:
    def __init__(self,id,name,emailId):
        self.__id=id
        self.__name=name
        self.__emailId=emailId
        self.__task=[]
    
    def addTask(self,task):
        self.__task.append(task)

    def getId(self):
        return self.__id
    
    def getName(self):
        return self.__name
    
    def getemailId(self):
        return self.__emailId
    
    def getTask(self):
        return self.__task
        