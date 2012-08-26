from .models import Duable
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

class Navigator(object):
    """ 
    The purpose of this class is to hold a logical interface to the data,
    interacting with the database, without regard to how this data is actually 
    displayed.

    For example, this class will keep track of which duable is currently selected.
    """
    
    def __init__(self, session):
        """
        Create a Navigator object.

        Parameters
        ----------
        session : sqlalchemy.Session
            A database session to the hw.db sqlite database.
        """
        self.session = session
        self.duable = None
        self.duables = []
        self.order_by = Duable.id

        #query parameters
        self.due_within = '3 days'
        self.name_like = '%'
        self.course_course = '' #to follow the conventions of byu, the course's
                                #name is simply 'course'

        self.views = (self._query_all, self._query_due, self._query_name,
                      self._query_course)
        self.view = self.views[0]
    
    def inc_duable(self, inc=1):
        if not self.duable or not self.duables:
            return
        newi = (self.duables.index(self.duable)+inc)%(len(self.duables))
        self.duable = self.duables[newi]

    def inc_views(self, inc=1):
        newi = (self.views.index(self.view)+inc)%(len(self.views)) 
        self.view = self.views[newi]

    def _process_query(self, query):
        """
        Put the results of the query into the interface.
        """
        self.duables = [duable for duable in query]
        if self.duable not in self.duables:
            if self.duables:
                self.duable = self.duables[0]
            else:
                self.duable = None

    def _base_query(self):
        return self.session.query(Duable).order_by(self.order_by)

    def _query_all(self):
        """
        Populate all duables.
        """
        self._process_query(self._base_query()) 

    def _query_due(self):
        """
        Populate duables within due parameters.
        """
        vals = self.due_within.split()
        param = {vals[1] : int(vals[0])}
        threshold = dt.now() + relativedelta(**param)
        query = self._base_query().filter(Duable.date_due < threshold)
        self._process_query(query)

    def _query_name(self):
        """
        Populate duables with name like the parameter.
        """
        query = self._base_query().filter(Duable.name.like(self.name_like))
        self._process_query(query)

    def _query_course(self):
        """
        Populate duables whose course has the specified value in field.
        """
        query = self._base_query().filter(Duable.course.has(
                                          course=self.course_course))
        self._process_query(query)
