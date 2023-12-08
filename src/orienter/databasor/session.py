from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from ..configurator import configuration
from ..databasor.models import *

engine = create_engine(f"sqlite:///{configuration.DATABASE_PATH}")
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

if __name__ == "__main__":
    stmt = select(User).where(User.user_id == 1)

    for user in session.scalars(stmt):
        print(user.first_name, user.last_name)
