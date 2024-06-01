from fastapi.testclient import TestClient
from .testdatabase import TestingSessionLocal
import random
import json
from datetime import datetime
from ..src.main import app, get_db

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

pnewid=str(random.randint(1,10000))
prandphone=str(random.randint(10000000000,99999999999))
presponse = client.post("/users/register",json={"nickname":"testuserzero","email":"testemail"+pnewid,"phone":prandphone,"password":"testpassword"})


def test_task_create():
    token = client.post("/users/login?nickname=testuserzero&password=testpassword")
    token=token.json()["token"]
    dogsid = client.get("/dogs/?token="+token)
    dogsid=int(dogsid.json()[-1]["id"])
    response = client.post("/task/create/?token="+token,json={"dog_id":dogsid,"type":"feed"})
    assert response.status_code == 200
    assert response.json()["success"] == "true"

def test_task_create_token_error():
    token="wrongtoken"
    response = client.post("/task/create/?token="+token,json={"dog_id":1,"type":"feed"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Wrong token"

def test_task_create_dog_not_found():
    token = client.post("/users/login?nickname=testuserzero&password=testpassword")
    token=token.json()["token"]
    dogsid=0
    response = client.post("/task/create/?token="+token,json={"dog_id":dogsid,"type":"feed"})
    assert response.status_code == 400
    assert response.json()["detail"] == "No such dog"

def test_get_tasks():
    token = client.post("/users/login?nickname=testuserzero&password=testpassword")
    token=token.json()["token"]
    response = client.get("/task/?token="+token)
    assert response.status_code == 200

def test_get_tasks_token_error():
    token="wrongtoken"
    response = client.get("/task/?token="+token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Wrong token"

def test_get_task():
    token = client.post("/users/login?nickname=testuserzero&password=testpassword")
    token=token.json()["token"]
    taskid = client.get("/task/?token="+token)
    taskid=str(taskid.json()[-1]["id"])
    response = client.get("/task/"+taskid+"/?token="+token)
    assert response.status_code == 200

def test_get_task_not_found():
    token = client.post("/users/login?nickname=testuserzero&password=testpassword")
    token=token.json()["token"]
    response = client.get("/task/-1/?token="+token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Task not found"

def test_get_task_error_token():
    token="wrongtoken"
    response = client.get("/task/0/?token="+token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Wrong token"

def test_task_change_status():
    token = client.post("/users/login?nickname=testuserzero&password=testpassword")
    token=token.json()["token"]
    taskid = client.get("/task/?token="+token)
    taskid=str(taskid.json()[-1]["id"])
    response = client.post("/task/"+taskid+"/change_status/?token="+token+"&status="+str(0))
    assert response.status_code == 200

def test_task_change_status_token_error():
    token="wrongtoken"
    taskid="-1"
    response = client.post("/task/"+taskid+"/change_status/?token="+token+"&status="+str(0))
    assert response.status_code == 400
    assert response.json()["detail"] == "Wrong token"

def test_task_change_status_error_id():
    token = client.post("/users/login?nickname=testuserzero&password=testpassword")
    token=token.json()["token"]
    taskid = client.get("/task/?token="+token)
    taskid="-1"
    response = client.post("/task/"+taskid+"/change_status/?token="+token+"&status="+str(0))
    assert response.status_code == 400
    assert response.json()["detail"] == "Task not found"


def test_add_task_response():
    token = client.post("/users/login?nickname=testuserzero&password=testpassword")
    token=token.json()["token"]
    taskid = client.get("/task/?token="+token)
    taskid=str(taskid.json()[-1]["id"])
    response = client.post("/task/"+taskid+"/responses/send/?token="+token,json={"proof":"testproof","delete":False})
    assert response.status_code == 200

def test_add_task_response_token_error():
    token="wrongtoken"
    taskid=str(0)
    response = client.post("/task/"+taskid+"/responses/send/?token="+token,json={"proof":"testproof","delete":False})
    assert response.status_code == 400
    assert response.json()["detail"] == "Wrong token"

def test_add_task_response_task_id_error():
    token = client.post("/users/login?nickname=testuserzero&password=testpassword")
    token=token.json()["token"]
    taskid=str(0)
    response = client.post("/task/"+taskid+"/responses/send/?token="+token,json={"proof":"testproof","delete":False})
    assert response.status_code == 400
    assert response.json()["detail"] == "Task not found"

def test_get_responses():
    token = client.post("/users/login?nickname=testuserzero&password=testpassword")
    token=token.json()["token"]
    response = client.get("/responses?token="+token)
    assert response.status_code == 200

def test_get_responses_token_error():
    token="wrongtoken"
    response = client.get("/responses?token="+token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Wrong token"

def test_get_esp_responses():
    token = client.post("/users/login?nickname=testuserzero&password=testpassword")
    token=token.json()["token"]
    taskid = client.get("/task/?token="+token)
    taskid=str(taskid.json()[-1]["id"])
    response = client.get("/task/"+taskid+"/responses/?token="+token)
    assert response.status_code == 200

def test_get_esp_responses_token_error():
    token="wrongtoken"
    taskid=str(0)
    response = client.get("/task/"+taskid+"/responses/?token="+token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Wrong token"

def test_delete_response_token_error():
    token="wrongtoken"
    response = client.post("/task/responses/"+str(0)+"/delete/?token="+token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Wrong token"

def test_delete_response_responseid_error():
    token = client.post("/users/login?nickname=testuserzero&password=testpassword")
    token=token.json()["token"]
    response = client.post("/task/responses/"+str(0)+"/delete/?token="+token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Reponse not found"

def test_delete_response():
    token = client.post("/users/login?nickname=testuserzero&password=testpassword")
    token=token.json()["token"]
    responseid = client.get("/responses/?token="+token)
    responseid=str(responseid.json()[-1]["id"])
    response = client.post("/task/responses/"+responseid+"/delete/?token="+token)
    assert response.status_code == 200
