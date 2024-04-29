from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    dog_id = Column(Integer, ForeignKey("dogs.id"))
    type = Column(String)
    status = Column(Boolean, default=True)

    responses = relationship("TaskResponse", back_populates="task")

class TaskResponse(Base):
    __tablename__ = "taskresponses"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    proof=Column(String)
    user_id=Column(Integer, ForeignKey("users.id"))
    delete=Column(Boolean, default=False)

    task=relationship("Task", back_populates="responses")