from User import User
from Task import Task, Priority
from UserService import UserService

user1 = User(101,"sathan","wfw@gmail.com")

task1 = Task(101,"write","write it efficiently","2hr", Priority.HIGH)
user1.addTask(task1)

service = UserService()

service.getAllTask(user1)
service.getPendingTask(user1)

service.completeTask(task1)

print(task1.getStatus())
