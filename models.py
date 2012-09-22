from sqlalchemy import (
    Column,
    ForeignKey,
    create_engine,
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

import os

DATABASE = os.path.expanduser('~/.hm.db')
engine = create_engine('sqlite:///%s' % (DATABASE), echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)

class Duable(Base):
    __tablename__ = 'duables'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    type = Column(String)
    post = Column(DateTime)
    due = Column(DateTime)
    done = Column(Boolean)
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship('Course', backref=backref('duables',
                          cascade='all, delete, delete-orphan',
                          order_by=due),
                          )

    def __init__(self, name):
        if not name:
            raise ValueError('Must give name.')
        self.name = name

    def __repr__(self):
        return "<Duable('%s')>" % (self.name)

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    course = Column(String, nullable=False)
    course_title = Column(String, nullable=False)
    sec = Column(String)
    hrs = Column(String)
    class_period = Column(String, nullable=False)
    days = Column(String, nullable=False)
    room = Column(String, nullable=False)
    bldg = Column(String, nullable=False)
    instructor = Column(String, nullable=False)

    def __repr__(self):
        return "<Course('%s')>" % (self.course)

    def __str__(self):
        return self.course
