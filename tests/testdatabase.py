from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..src.database import Base
from ..src.users import models as usersmodels
from ..src.users import schemas as usersschemas
from ..src.dogs import models as dogsmodels
from ..src.dogs import schemas as dogsschemas
from ..src.tasks import models as tasksmodels
from ..src.tasks import schemas as tasksschemas

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
Base.metadata.create_all(bind=engine)
usersmodels.Base.metadata.create_all(bind=engine)
dogsmodels.Base.metadata.create_all(bind=engine)
tasksmodels.Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

