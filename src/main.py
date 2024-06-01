from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
import hashlib
import socket
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

from . import crud
from .users import models as usersmodels
from .users import schemas as usersschemas
from .dogs import models as dogsmodels
from .dogs import schemas as dogsschemas
from .tasks import models as tasksmodels
from .tasks import schemas as tasksschemas
from .database import SessionLocal, engine

usersmodels.Base.metadata.create_all(bind=engine)
dogsmodels.Base.metadata.create_all(bind=engine)
tasksmodels.Base.metadata.create_all(bind=engine)

#hashed host ip
#hashhost=hashlib.md5(socket.gethostname().encode()).hexdigest()

#logger parameters
FORMATTER_STRING = "%(asctime)s - %(haship)s - %(name)s - %(levelname)s - %(message)s"
FORMATTER = logging.Formatter(FORMATTER_STRING)
LOG_FILE = "./mobiledogsapplogs.log"

#function for logger creating
def get_logger(logger_name,haship):
    extra = {'haship':haship}
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    logger.addHandler(console_handler)

    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    logger.addHandler(file_handler)
    logger = logging.LoggerAdapter(logger, extra)
    return logger


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/register")
def create_user(request: Request, user: usersschemas.UserCreate, db: Session = Depends(get_db)):
    if (request.client is None):
        ip="0"
    else:
        ip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)

    logger.info("Sent request to register new user")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        logger.error("Entered Email already registered")
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        logger.debug("Email verifed")
    db_user = crud.get_user_by_phone(db, phone=user.phone)
    if db_user:
        logger.error("Entered phone number already registered")
        raise HTTPException(status_code=400, detail="Phone already registered")
    else:
        logger.debug("Phone number verifed")
    db_user = crud.get_user_by_nickname(db, nickname=user.nickname)
    if db_user:
        logger.error("Entered nickname already registered")
        raise HTTPException(status_code=400, detail="Nickname already registered")
    else:
        logger.debug("Nickname verifed")
    db_user=crud.create_user(db=db, user=user)
    logger.info('New user "'+db_user.nickname+'" created')
    return {"nickname":db_user.nickname,"token":db_user.token}

@app.post("/users/login")
def login_user(request: Request, nickname:str,password:str, db: Session = Depends(get_db)):
    if (request.client is None):
        ip="0"
    else:
        ip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to login")
    db_user=crud.get_users_token(db=db,nickname=nickname,password=password)
    if db_user is None:
         logger.error("Wrong entered nickname or password")
         raise HTTPException(status_code=400, detail="Wrong nickname or password")
    else:
        logger.info('User "'+db_user.nickname+'" logined')
    return {"nickname":db_user.nickname,"token":db_user.token}


@app.get("/users/", response_model=list[usersschemas.User])
def read_users(request: Request, token:str,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if (request.client is None):
        ip="0"
    else:
        ip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info(str(ip)+" Sent request to get list of users")
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error("Wrong entered token")
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.info("Correct entered token")
    users = crud.get_users(db, skip=skip, limit=limit)
    for user in users:
       user.token="secret"
    return users


@app.get("/users/{user_id}", response_model=usersschemas.User)
def read_user(request: Request, token:str,user_id: int, db: Session = Depends(get_db)):
    if (request.client is None):
        ip="0"
    else:
        ip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to get user by id "+str(user_id))
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error("Wrong entered token")
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.info("Correct entered token")
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        logger.error("User not found by id "+str(user_id))
        raise HTTPException(status_code=400, detail="User not found")
    else:
        logger.info("User found by id "+str(user_id))
    db_user.token="secret"
    return db_user

@app.post("/dogs/register")
def create_dog(request: Request, token:str,dog: dogsschemas.DogCreate, db: Session = Depends(get_db)):
    if (request.client is None):
        ip="0"
    else:
        ip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to register new dog")
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error("Wrong entered token")
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.info("Correct entered token")
    db_dog = crud.get_dog_by_collar_id(db, collar_id=dog.collar_id)
    if db_dog:
        logger.error('Dog with collar id "'+str(dog.collar_id)+'" already registered')
        raise HTTPException(status_code=400, detail="Dog with this collar already registered")
    else:
        logger.debug('Collar with id "'+str(dog.collar_id)+'" is free')
    db_collar=crud.get_collar(db, collar_id=dog.collar_id)
    if db_collar is None:
        logger.error('Collar with id "'+str(dog.collar_id)+'" does not exist')
        raise HTTPException(status_code=400, detail="No such collar")
    else:
        logger.debug('Collar with id "'+str(dog.collar_id)+'" exist')
    dog=crud.create_dog(db=db, dog=dog)
    logger.info('Dog registered on collar with id "'+str(dog.collar_id)+'"')
    return {"success":"true","exception":"null","dog_id":dog.id}


@app.get("/dogs/", response_model=list[dogsschemas.Dog])
def read_dogs(request: Request, token:str,near:bool=False,latitude:str ="0", longitude:str="0",skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if (request.client is None):
        ip="0"
    else:
        ip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)

    logger.info("Sent request to get list of dogs")
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error('Wrong entered token')
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.debug("Correct entered token")
    if near:
       logger.info("Some dogs near to user")
       dogs = crud.get_near_dogs(db,latitude=latitude , longitude=longitude , skip=skip, limit=limit)
    else:
       logger.info("No dogs near to user")
       dogs = crud.get_dogs(db, skip=skip, limit=limit)
    return dogs

@app.get("/dogs/{dog_id}", response_model=dogsschemas.Dog)
def read_dog(request: Request, token:str,dog_id: int, db: Session = Depends(get_db)):
    if (request.client is None):
        ip="0"
    else:
        ip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to get dog by id")
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error('Wrong entered token')
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.debug("Correct entered token")
    db_dog = crud.get_dog(db, dog_id=dog_id)
    if db_dog is None:
        logger.error('Dog with id "'+str(dog_id)+'" not found')
        raise HTTPException(status_code=400, detail="Dog not found")
    else:
        logger.info('Dog with id "'+str(dog_id)+'" found')
    return db_dog

@app.post("/collars/register")
def create_collar(request: Request, token:str,collar: dogsschemas.CollarCreate, db: Session = Depends(get_db)):
    if (request.client is None):
        ip="0"
    else:
        ip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)

    logger.info("Sent request to register collar")
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error('Wrong entered token')
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.debug("Correct entered token")
    db_collar = crud.get_collar_by_ip(db, ip=collar.ip)
    if db_collar:
        logger.error('Collar with ip "'+str(collar.ip)+'" already exists')
        raise HTTPException(status_code=400, detail="Collar with this ip already registered")
    else:
        logger.debug('IP "'+str(collar.ip)+'" is free')
    collar=crud.create_collar(db=db, collar=collar)
    logger.info('Collar with ip"'+str(collar.ip)+'" succesfully registered')
    return {"success":"true","exception":"null","id":collar.id}


@app.get("/collars/", response_model=list[dogsschemas.Collar])
def read_collars(request: Request, token:str,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if (request.client is None):
        ip="0"
    else:
        ip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to get collars")
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error('Wrong entered token')
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.debug("Correct entered token")
    collars = crud.get_collars(db, skip=skip, limit=limit)
    logger.info('Collars returned')
    return collars


@app.get("/collars/{collar_id}", response_model=dogsschemas.Collar)
def read_collar(request: Request, token:str,collar_id: int, db: Session = Depends(get_db)):
    if (request.client is None):
        ip="0"
    else:
        ip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to get collar by id")
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error('Wrong entered token')
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.debug("Correct entered token")
    db_collar = crud.get_collar(db, collar_id=collar_id)
    if db_collar is None:
        logger.error('Collar with id "'+str(collar_id)+'" not found')
        raise HTTPException(status_code=400, detail="Collar not found")
    else:
        logger.debug('Collar with id "'+str(collar_id)+'" found')
    logger.info('Collar with id "'+str(collar_id)+'" returned')
    return db_collar

@app.get("/collars/getbyip/{collar_ip}", response_model=dogsschemas.Collar)
def read_collar(request: Request, collar_ip:str,token:str, db: Session = Depends(get_db)):
    if (request.client is None):
        ip="0"
    else:
        ip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to get collar by ip")
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error('Wrong entered token')
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.debug("Correct entered token")
    db_collar = crud.get_collar_by_ip(db, ip=collar_ip)
    if db_collar is None:
        logger.error('Collar with ip "'+str(collar_ip)+'" not found')
        raise HTTPException(status_code=400, detail="Collar not found")
    else:
        logger.debug('Collar with ip "'+collar_ip+'" found')
    logger.info('Collar with ip "'+str(collar_ip)+'" returned')
    return db_collar


@app.post("/dogs/{dog_id}/data", response_model=dogsschemas.DogsData)
def create_data_for_dog(
    request: Request, ip:str,dog_id: int, item: dogsschemas.DogsDataCreate, db: Session = Depends(get_db)
):
    if (request.client is None):
        clientip="0"
    else:
        clientip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to post data about dog using ip")
    db_collar = crud.get_collar_by_ip(db, ip=ip)
    if db_collar is None:
        logger.error('Collar with ip "'+str(ip)+'" not found')
        raise HTTPException(status_code=400, detail="Wrong ip")
    logger.info('Succesfully posted information about dog using ip "'+ip+'"')
    return crud.create_dogs_data(db=db, item=item, dog_id=dog_id)

@app.get("/dogs/{dog_id}/status", response_model=list[dogsschemas.DogsData])
def get_data_for_dog(
    request: Request, token:str,dog_id: int, db: Session = Depends(get_db)
):
    if (request.client is None):
        clientip="0"
    else:
        clientip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to get dog status")

    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error('Wrong entered token')
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.debug("Correct entered token")
    logger.info('Returned status about dog with id "'+str(dog_id)+'"')
    return crud.get_that_dogs_data(db=db, dog_id=dog_id)


@app.get("/data", response_model=list[dogsschemas.DogsData])
def read_dogsdata(request: Request, token:str,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if (request.client is None):
        clientip="0"
    else:
        clientip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to get dogs data")
    
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error('Wrong entered token')
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.debug("Correct entered token")
    items = crud.get_dogs_data(db, skip=skip, limit=limit)
    logger.info('Returned dogs data')
    return items

@app.post("/task/create")
def create_task(request: Request, token:str,task: tasksschemas.TaskCreate, db: Session = Depends(get_db)):
    if (request.client is None):
        clientip="0"
    else:
        clientip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to create new task")

    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error('Wrong entered token')
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.debug("Correct entered token")
    dog=crud.get_dog(db, dog_id=task.dog_id)
    if dog is None:
        logger.error('Dog with id "'+str(task.dog_id)+'" not found')
        raise HTTPException(status_code=400, detail="No such dog")
    else:
        logger.debug('Dog with id "'+str(task.dog_id)+'" found')

    task=crud.create_task(db=db, task=task)
    logger.info('New task created')
    return {"success":"true","exception":"null","task_id":task.id}


@app.get("/task", response_model=list[tasksschemas.Task])
def read_tasks(request: Request, token:str,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if (request.client is None):
        clientip="0"
    else:
        clientip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to get info about task")
    
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error('Wrong entered token')
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.debug("Correct entered token")
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    logger.info('Info returned')
    return tasks


@app.get("/task/{task_id}", response_model=tasksschemas.Task)
def read_task(request: Request, token:str,task_id: int, db: Session = Depends(get_db)):
    if (request.client is None):
        clientip="0"
    else:
        clientip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to get info about task by id")

    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error('Wrong entered token')
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.debug("Correct entered token")
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        logger.error('Task with id "'+str(task_id)+'" not found')
        raise HTTPException(status_code=400, detail="Task not found")
    else:
        logger.debug('Task with id "'+str(task_id)+'" found')
    logger.info('Info about task with id "'+str(task_id)+'" returned')
    return db_task

@app.post("/task/{task_id}/change_status")
def change_task(request: Request, token:str,task_id: int,status:bool, db: Session = Depends(get_db)):
    if (request.client is None):
        clientip="0"
    else:
        clientip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to change status of task with id")

    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error('Wrong entered token')
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.debug("Correct entered token")
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        logger.error('Task with id "'+str(task_id)+'" not found')
        raise HTTPException(status_code=400, detail="Task not found")
    else:
        logger.debug('Task with id "'+str(task_id)+'" found')
    task=crud.change_task_status(db=db, task_id=task_id,status=status)
    logger.info('Status of task with id "'+str(task_id)+'" changed')
    return {"success":"true","exception":"null","task_id":task.id}


@app.post("/task/{task_id}/responses/send", response_model=tasksschemas.TaskResponse)
def create_task_response(
    request: Request, token:str,task_id:int,item: tasksschemas.TaskResponseCreate, db: Session = Depends(get_db)
):
    if (request.client is None):
        clientip="0"
    else:
        clientip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to sent task response")

    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error('Wrong entered token')
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.debug("Correct entered token")
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        logger.error('Task with id "'+str(task_id)+'" not found')
        raise HTTPException(status_code=400, detail="Task not found")
    else:
        logger.debug('Task with id "'+str(task_id)+'" found')
    logger.info('Response to task with id "'+str(task_id)+'" sent')
    return crud.create_task_response(db=db, item=item, task_id=task_id,user_id=tokencheck.id)

@app.post("/task/responses/{response_id}/delete")
def change_task(request: Request, token:str,response_id: int, db: Session = Depends(get_db)):
    if (request.client is None):
        clientip="0"
    else:
        clientip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to delete task response")

    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error('Wrong entered token')
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.debug("Correct entered token")
    db_response = crud.get_task_response(db, response_id=response_id)
    if db_response is None:
        logger.error('Response with id "'+str(response_id)+'" not found')
        raise HTTPException(status_code=400, detail="Reponse not found")
    else:
        logger.debug('Response with id "'+str(response_id)+'" found')
    response=crud.change_response_status(db=db, response_id=response_id,status=1)
    logger.info('Response with id "'+str(response_id)+'" deleted')
    return {"success":"true","exception":"null","response_id":response.id}


@app.get("/task/{task_id}/responses", response_model=list[tasksschemas.TaskResponse])
def get_task_responses(
    request: Request, token:str,task_id: int, db: Session = Depends(get_db)
):
    if (request.client is None):
        clientip="0"
    else:
        clientip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to get all responses to one task")

    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error('Wrong entered token')
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.debug("Correct entered token")
    logger.info('Responses to task with id "'+str(task_id)+'" returned')    
    return crud.get_that_task_responses(db=db, task_id=task_id)


@app.get("/responses", response_model=list[tasksschemas.TaskResponse])
def read_task_responses(request: Request, token:str,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if (request.client is None):
        clientip="0"
    else:
        clientip = request.client.host
    haship=hashlib.md5(str(ip).encode()).hexdigest()
    logger = get_logger("create_user",haship)
    logger.info("Sent request to get all responses")
    
    tokencheck = crud.get_user_by_token(db, token=token)
    if tokencheck is None:
        logger.error('Wrong entered token')
        raise HTTPException(status_code=400, detail="Wrong token")
    else:
        logger.debug("Correct entered token")
    items = crud.get_task_responses(db, skip=skip, limit=limit)
    logger.info("All responses returned")
    return items