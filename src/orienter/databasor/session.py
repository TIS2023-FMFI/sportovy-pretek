from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from . import models
from ..configurator import configuration

engine = create_engine(f"sqlite:///{configuration.DATABASE_PATH}")
Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    with Session.begin() as session:
        # section_schema = SectionSchema()
        # data = section_schema.load({'id': 244, 'nazov': "HELO"}, session=session)
        # print(data)
        stmt = select(models.User).where(models.User.user_id == 14)
        for user in session.scalars(stmt):
            print(user)
