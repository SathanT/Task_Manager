from backend.Task import TaskStatus

class UserService:

    def getAllTask(self,user):
        task=user.getAllTask()
        for i in task:
            print(i.getName())
    
    def getPendingTask(self,user):
        task=user.getAllTask()
        for i in task:
            if TaskStatus.PENDING==i.getStatus():
                print(i.getName())

    def completTask(self,task):
        task.setTaskStatus(TaskStatus.COMPLETED)