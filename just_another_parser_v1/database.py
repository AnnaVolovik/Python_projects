from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#create an engine that stores data in the local directory's file
engine = create_engine('sqlite:///just_another_parser_v1/just_another_parser_v1.db', convert_unicode=True) #the db name - location
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import just_another_parser_v1.models
    Base.metadata.create_all(bind=engine)
