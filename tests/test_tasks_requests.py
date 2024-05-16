from fastapi.testclient import TestClient
import random
import json
from datetime import datetime
from ..src.main import app

client = TestClient(app)

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
    response = client.get("/task/0/?token="+token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Task not found"

def test_get_task_not_found():
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
    assert response.json()["detail"] == "There isn't such dog's id"

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
