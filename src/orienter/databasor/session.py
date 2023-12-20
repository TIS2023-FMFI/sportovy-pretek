from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .schemas import *
from ..configurator import configuration

engine = create_engine(f"sqlite:///{configuration.DATABASE_PATH}")
Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    with Session.begin() as session:
        section_schema = SectionSchema()
        data = section_schema.load({'id': 244, 'nazov': "HELO"}, session=session)
        print(data)
