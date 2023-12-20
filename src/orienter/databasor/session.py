from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, mapper, scoped_session

from .models import *
from .schemas import *
from ..configurator import configuration

engine = create_engine(f"sqlite:///{configuration.DATABASE_PATH}")
Session = sessionmaker(bind=engine)
session = scoped_session(Session)
event.listen(mapper, "after_configured", setup_schema(Base, session))
Base.metadata.create_all(engine)


if __name__ == "__main__":
    section_schema = Section.__marshmallow__()
    data = section_schema.load({'id': 244, 'nazov': "HELO"}, session=session)
    print(data)
