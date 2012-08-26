from .models import Duable
from .views import *

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

        self.views = [View_all(), View_due(), View_name(), View_course()]
        self.view = self.views[0]
    
        self.order_by = Duable.id
        self.show_done = True

    def inc_duable(self, inc=1):
        if not self.duable or not self.duables:
            return
        newi = (self.duables.index(self.duable)+inc)%(len(self.duables))
        self.duable = self.duables[newi]

    def inc_views(self, inc=1):
        if not self.view or not self.views:
            return
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
        if self.show_done:
            return self.session.query(Duable).order_by(self.order_by)
        else:
            query = self.session.query(Duable).order_by(self.order_by)
            return query.filter(Duable.done == False)

    def query(self):
        self._process_query(self.view.filter(self._base_query()))
