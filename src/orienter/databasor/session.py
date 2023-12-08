from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from ..configuration import configuration
from ..databasor import models

engine = create_engine(f"sqlite:///{configuration.DATABASE_PATH}")
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

stmt = select(models.User)

for user in session.scalars(stmt):
     print(user.first_name)
