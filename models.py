from sqlalchemy import (
    Column,
    ForeignKey,
    )

from sqlalchemy.types import (
    Integer,
    String,
    DateTime,
    Boolean,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    backref,
    relationship,
    scoped_session,
    sessionmaker,
    )

from sqlalchemy import sessionmaker
from datetime import datetime

DATABASE = 'hw.db'
engine = create_engine('sqlite:///%s' % (DATABASE), echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Duable(Base):
    __tablename__ = 'duables'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    date_open = Column(DateTime) #if there is a window in which it can be done
    date_due = Column(DateTime)
    done = Column(Boolean)

    def __init__(name):
        if not name:
            raise ValueError('Must give name.')
        self.name = name

    def __repr(self):
        return "<Duable('%s')>" % (self.name)
