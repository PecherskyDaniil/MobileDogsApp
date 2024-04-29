from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import hashlib

import crud
from users import models as usersmodels
from users import schemas as usersschemas
from dogs import models as dogsmodels
from dogs import schemas as dogsschemas
from tasks import models as tasksmodels
from tasks import schemas as tasksschemas
from database import SessionLocal, engine

usersmodels.Base.metadata.create_all(bind=engine)
dogsmodels.Base.metadata.create_all(bind=engine)
tasksmodels.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/register")
def create_user(user: usersschemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.get_user_by_phone(db, phone=user.phone)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone already registered")
    db_user = crud.get_user_by_nickname(db, nickname=user.nickname)
    if db_user:
        raise HTTPException(status_code=400, detail="Nickname already registered")
    db_user=crud.create_user(db=db, user=user)
    return {"nickname":db_user.nickname,"token":db_user.token}

@app.post("/users/login")
def login_user(nickname:str,password:str, db: Session = Depends(get_db)):
    db_user=crud.get_users_token(db=db,nickname=nickname,password=password)
    if db_user is None:
         raise HTTPException(status_code=400, detail="Wrong nickname or password")
    return {"nickname":db_user.nickname,"token":db_user.token}


@app.get("/users/", response_model=list[usersschemas.User])
def read_users(token:str,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    users = crud.get_users(db, skip=skip, limit=limit)
    for user in users:
       user.token="secret"
    return users


@app.get("/users/{user_id}", response_model=usersschemas.User)
def read_user(token:str,user_id: int, db: Session = Depends(get_db)):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.token="secret"
    return db_user

@app.post("/dogs/")
def create_dog(token:str,dog: dogsschemas.DogCreate, db: Session = Depends(get_db)):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    db_dog = crud.get_dog_by_collar_id(db, collar_id=dog.collar_id)
    if db_dog:
        raise HTTPException(status_code=400, detail="Dog with this collar already registered")
    db_collar=crud.get_collar(db, collar_id=dog.collar_id)
    if db_collar is None:
        raise HTTPException(status_code=400, detail="No such collar")
    dog=crud.create_dog(db=db, dog=dog)
    return {"succes":"true","exception":"null","dog_id":dog.id}


@app.get("/dogs/", response_model=list[dogsschemas.Dog])
def read_dogs(token:str,near:bool=False,latitude:str ="0", longitude:str="0",skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    if near:
       dogs = crud.get_near_dogs(db,latitude=latitude , longitude=longitude , skip=skip, limit=limit)
    else:
       dogs = crud.get_dogs(db, skip=skip, limit=limit)
    return dogs

@app.get("/dogs/{dog_id}", response_model=dogsschemas.Dog)
def read_dog(token:str,dog_id: int, db: Session = Depends(get_db)):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    db_dog = crud.get_dog(db, dog_id=dog_id)
    if db_dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    return db_dog

@app.post("/collars/")
def create_collar(token:str,collar: dogsschemas.CollarCreate, db: Session = Depends(get_db)):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    db_collar = crud.get_collar_by_ip(db, ip=collar.ip)
    if db_collar:
        raise HTTPException(status_code=400, detail="Collar with this ip already registered")
    collar=crud.create_collar(db=db, collar=collar)
    return {"success":"true","exception":"null"}


@app.get("/collars/", response_model=list[dogsschemas.Collar])
def read_collars(token:str,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    collars = crud.get_collars(db, skip=skip, limit=limit)
    return collars


@app.get("/collars/{collar_id}", response_model=dogsschemas.Dog)
def read_collar(token:str,collar_id: int, db: Session = Depends(get_db)):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    db_collar = crud.get_collar(db, collar_id=collar_id)
    if db_collar is None:
        raise HTTPException(status_code=404, detail="Collar not found")
    return db_collar


@app.post("/dogs/{dog_id}/data/", response_model=dogsschemas.DogsData)
def create_data_for_dog(
    ip:str,dog_id: int, item: dogsschemas.DogsDataCreate, db: Session = Depends(get_db)
):
    db_collar = crud.get_collar_by_ip(db, ip=ip)
    if db_collar is None:
        raise HTTPException(status_code=400, detail="Wrong ip")
    return crud.create_dogs_data(db=db, item=item, dog_id=dog_id)

@app.get("/dogs/{dog_id}/data/", response_model=list[dogsschemas.DogsData])
def get_data_for_dog(
    token:str,dog_id: int, db: Session = Depends(get_db)
):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    
    return crud.get_that_dogs_data(db=db, dog_id=dog_id)


@app.get("/data/", response_model=list[dogsschemas.DogsData])
def read_dogsdata(token:str,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    items = crud.get_dogs_data(db, skip=skip, limit=limit)
    return items

@app.post("/task/create/")
def create_task(token:str,task: tasksschemas.TaskCreate, db: Session = Depends(get_db)):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    dog=crud.get_dog(db, dog_id=task.dog_id)
    if dog is None:
        raise HTTPException(status_code=404, detail="No such dog")

    task=crud.create_task(db=db, task=task)
    return {"success":"true","exception":"null","task_id":task.id}


@app.get("/task/", response_model=list[tasksschemas.Task])
def read_tasks(token:str,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


@app.get("/task/{task_id}", response_model=tasksschemas.Task)
def read_task(token:str,task_id: int, db: Session = Depends(get_db)):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.post("/task/{task_id}/change_status")
def change_task(token:str,task_id: int,status:bool, db: Session = Depends(get_db)):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task=crud.change_task_status(db=db, task_id=task_id,status=status)
    return {"success":"true","exception":"null","task_id":task.id}


@app.post("/task/{task_id}/responses/", response_model=tasksschemas.TaskResponse)
def create_task_response(
    token:str,task_id:int,item: tasksschemas.TaskResponseCreate, db: Session = Depends(get_db)
):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=400, detail="There isn't such dog's id")
    return crud.create_task_response(db=db, item=item, task_id=task_id,user_id=tokencheck.id)

@app.post("/task/responses/{response_id}/delete")
def change_task(token:str,response_id: int, db: Session = Depends(get_db)):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    db_response = crud.get_task_response(db, response_id=response_id)
    if db_response is None:
        raise HTTPException(status_code=404, detail="Reponse not found")
    response=crud.change_response_status(db=db, response_id=response_id,status=1)
    return {"success":"true","exception":"null","response_id":response.id}


@app.get("/task/{task_id}/responses/", response_model=list[tasksschemas.TaskResponse])
def get_task_responses(
    token:str,task_id: int, db: Session = Depends(get_db)
):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    
    return crud.get_that_task_responses(db=db, task_id=task_id)


@app.get("/responses/", response_model=list[tasksschemas.TaskResponse])
def read_task_responses(token:str,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        raise HTTPException(status_code=404, detail="Wrong token")
    items = crud.get_task_responses(db, skip=skip, limit=limit)
    return items