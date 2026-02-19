import requests
name="sathan"
email="wonfowrerg"
ur="http://127.0.0.1:8000/users"
u={
    "name":name,
    "email":email
}
req=requests.post(ur,json=u)
user=req.json()
user_id=user["id"]
task_ur=f"http://127.0.0.1:8000/task/{user_id}"
task={
    "name":"writing",
    "description":"write neatly",
    "duration":"2hour"   
}
req=requests.post(task_ur,json=task)
print(req.status_code)
print(req.json())