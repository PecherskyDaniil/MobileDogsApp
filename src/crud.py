from sqlalchemy.orm import Session
import hashlib
from .users import models as usersmodels
from .users import schemas as usersschemas
from .dogs import models as dogsmodels
from .dogs import schemas as dogsschemas
from .tasks import models as tasksmodels
from .tasks import schemas as tasksschemas



def get_user(db: Session, user_id: int):
    return db.query(usersmodels.User).filter(usersmodels.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(usersmodels.User).filter(usersmodels.User.email == email).first()

def get_user_by_nickname(db: Session, nickname: str):
    return db.query(usersmodels.User).filter(usersmodels.User.nickname == nickname).first()

def get_user_by_phone(db: Session, phone: str):
    return db.query(usersmodels.User).filter(usersmodels.User.phone == phone).first()

def get_user_by_token(db: Session, token: str):
    return db.query(usersmodels.User).filter(usersmodels.User.token == token).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(usersmodels.User).offset(skip).limit(limit).all()

def get_users_token(db: Session, nickname: str,password:str):
    return db.query(usersmodels.User).filter(usersmodels.User.nickname == nickname).filter(usersmodels.User.hashed_password == password+"notreallyhashed").first()

def create_user(db: Session, user: usersschemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = usersmodels.User(email=user.email,phone=user.phone, nickname=user.nickname, hashed_password=fake_hashed_password,token=hashlib.md5((user.nickname+user.password).encode()).hexdigest())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_dog(db: Session, dog_id: int):
    return db.query(dogsmodels.Dog).filter(dogsmodels.Dog.id == dog_id).first()

def get_dog_by_collar_id(db: Session, collar_id: int):
    return db.query(dogsmodels.Dog).filter(dogsmodels.Dog.collar_id == collar_id).first()

def get_dogs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(dogsmodels.Dog).offset(skip).limit(limit).all()

def get_near_dogs(db: Session, latitude:str , longitude:str , skip: int = 0, limit: int = 100):
	dogs=db.query(dogsmodels.Dog).offset(skip).limit(limit).all()
	answer=[]
	for dog in dogs:
            if (len(dog.datas)>0):
                if (abs(float(dog.datas[-1].latitude)-float(latitude))<=1 and abs(float(dog.datas[-1].longitude)-float(longitude))<=1):
                    answer.append(dog)
	return answer


def create_dog(db: Session, dog: dogsschemas.DogCreate):
    db_dog = dogsmodels.Dog(name=dog.name,description=dog.description, collar_id=dog.collar_id)
    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)
    return db_dog

def get_collar(db: Session, collar_id: int):
    return db.query(dogsmodels.Collar).filter(dogsmodels.Collar.id == collar_id).first()

def get_collar_by_ip(db: Session, ip: str):
    return db.query(dogsmodels.Collar).filter(dogsmodels.Collar.ip == ip).first()

def get_collars(db: Session, skip: int = 0, limit: int = 100):
    return db.query(dogsmodels.Collar).offset(skip).limit(limit).all()

def create_collar(db: Session, collar: dogsschemas.CollarCreate):
    db_collar = dogsmodels.Collar(ip=collar.ip)
    db.add(db_collar)
    db.commit()
    db.refresh(db_collar)
    return db_collar

def get_dogs_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(dogsmodels.DogsData).offset(skip).limit(limit).all()

def get_that_dogs_data(db: Session, dog_id:int):
    return db.query(dogsmodels.DogsData).filter(dogsmodels.DogsData.dog_id == dog_id).all()

def create_dogs_data(db: Session, item: dogsschemas.DogsDataCreate, dog_id: int):
    db_data = dogsmodels.DogsData(**item.dict(), dog_id=dog_id)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def get_task(db: Session, task_id: int):
    return db.query(tasksmodels.Task).filter(tasksmodels.Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(tasksmodels.Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: tasksschemas.TaskCreate):
    db_task = tasksmodels.Task(dog_id=task.dog_id,type=task.type)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def change_task_status(db: Session, task_id: int,status:bool):
    db_task=db.query(tasksmodels.Task).filter(tasksmodels.Task.id == task_id).first()
    db_task.status=status
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task_responses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(tasksmodels.TaskResponse).filter(tasksmodels.TaskResponse.delete==0).offset(skip).limit(limit).all()

def get_task_response(db: Session, response_id:int):
    return db.query(tasksmodels.TaskResponse).filter(tasksmodels.TaskResponse.id == response_id).first()

def get_that_task_responses(db: Session, task_id:int):
    return db.query(tasksmodels.TaskResponse).filter(tasksmodels.TaskResponse.task_id == task_id).filter(tasksmodels.TaskResponse.delete==0).all()

def create_task_response(db: Session, item: tasksschemas.TaskResponseCreate, task_id: int,user_id:int):
    db_taskresponse = tasksmodels.TaskResponse(**item.dict(), task_id=task_id,user_id=user_id)
    db.add(db_taskresponse)
    db.commit()
    db.refresh(db_taskresponse)
    return db_taskresponse

def change_response_status(db: Session, response_id: int,status:bool):
    db_response=db.query(tasksmodels.TaskResponse).filter(tasksmodels.TaskResponse.id == response_id).first()
    db_response.delete=status
    db.commit()
    db.refresh(db_response)
    return db_response
