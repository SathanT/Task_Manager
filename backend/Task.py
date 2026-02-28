from enum import Enum

class TaskStatus(str,Enum):
    PENDING="pending"
    COMPLETED="completed"

class Priority(str,Enum):
    HIGH="HIGH"
    MEDIUM="MEDIUM"
    LOW="LOW"

class Task:
    def __init__(self,id,name,description,duration,priority : Priority):
        self.__id=id
        self.__name=name
        self.__description=description
        self.__duration=duration
        self.__priority=priority
        self.__status=TaskStatus.PENDING

    def getId(self):
        return self.__id
    
    def getName(self):
        return self.__name
    
    def getDuration(self):
        return self.__duration
    
    def getStatus(self):
        return self.__status
    
    def setTaskStatus(self,status):
        self.__status = status

    def completeTask(self):
        self.__status = TaskStatus.COMPLETED
