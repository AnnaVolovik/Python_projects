from sqlalchemy import Column, Integer, String
from just_another_parser_v1.database import Base

class Entries(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True) 
    url = Column(String(250), nullable = False) #do we need to consider long URLs, like 2,083 characters?
    all_tags = Column(Integer, nullable = False)
    a_tags = Column(Integer, nullable = False)
    div_tags = Column(Integer, nullable = False)

    def __init__(self, url, all_tags,a_tags,div_tags):
        self.url = url
        self.all_tags = all_tags
        self.a_tags = a_tags
        self.div_tags = div_tags


