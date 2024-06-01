from fastapi.testclient import TestClient
from .testdatabase import TestingSessionLocal
import random
from ..src.main import app,get_db

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_user_register():
    newid=str(random.randint(1,10000))
    randphone=str(random.randint(10000000000,99999999999))
    response = client.post("/users/register",json={"nickname":"testuser"+newid,"email":"testemail"+newid+"@gmail.com","phone":randphone,"password":"testpassword"})
    assert response.status_code == 200
    assert response.json()["nickname"] == "testuser"+newid

def test_user_register_nickname_error():
    newid=str(random.randint(1,10000))
    randphone=str(random.randint(10000000000,99999999999))
    response = client.post("/users/register",json={"nickname":"testuserzero","email":"testemail"+newid,"phone":randphone,"password":"testpassword"})
    response = client.post("/users/register",json={"nickname":"testuserzero","email":"testemail"+newid,"phone":randphone,"password":"testpassword"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Nickname already registered"
def test_user_register_email_error():
    newid=str(random.randint(1,10000))
    randphone=str(random.randint(10000000000,99999999999))
    response = client.post("/users/register",json={"nickname":"testuser"+newid,"email":"testemailzero@gmail.com","phone":randphone,"password":"testpassword"})
    response = client.post("/users/register",json={"nickname":"testuser"+newid,"email":"testemailzero@gmail.com","phone":randphone,"password":"testpassword"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_user_register_phone_error():
    newid=str(random.randint(1,10000))
    randphone=str(random.randint(10000000000,99999999999))
    response = client.post("/users/register",json={"nickname":"testuser"+newid,"email":"testemail2"+newid,"phone":"00000000000","password":"testpassword"})
    response = client.post("/users/register",json={"nickname":"testuser"+newid,"email":"testemail"+newid,"phone":"00000000000","password":"testpassword"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Phone already registered"

def test_user_login():
    response = client.post("/users/login?nickname=testuserzero&password=testpassword")
    assert response.status_code == 200
    assert response.json()["nickname"] == "testuserzero"

def test_user_login_wrong_password_error():
    response = client.post("/users/login?nickname=testuserzero&password=wrongpassword")
    assert response.status_code == 400
    assert response.json()["detail"] == "Wrong nickname or password"

def test_get_users():
    token = client.post("/users/login?nickname=testuserzero&password=testpassword")
    token=token.json()["token"]
    response = client.get("/users?token="+token)
    assert response.status_code == 200

def test_get_users_token_error():
    token="wrongtoken"
    response = client.get("/users?token="+token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Wrong token"

def test_get_user():
    token = client.post("/users/login?nickname=testuserzero&password=testpassword")
    token=token.json()["token"]
    response = client.get("/users/1?token="+token)
    assert response.status_code == 200

def test_get_user_token_error():
    token="wrongtoken"
    response = client.get("/users/1?token="+token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Wrong token"

def test_get_user_user_not_found():
    token = client.post("/users/login?nickname=testuserzero&password=testpassword")
    token=token.json()["token"]
    response = client.get("/users/-100?token="+token)
    assert response.status_code == 400
    assert response.json()["detail"] == "User not found"







