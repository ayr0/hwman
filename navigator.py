from .models import Duable
from .views import *
from datetime import datetime

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

        self.duables = []
        self.duable = None

        self.views = [View_all(), 
                      View_due(), 
                      View_name(), 
                      View_course(),
                      ]
        self.view = self.views[0]
    
        self.show_done = False 
        self.show_all_post = False

        self.cols = [Duable.name, 
                     Duable.type, 
                     Duable.post,
                     Duable.due,
                     Duable.course,
                     ]
        self.col = self.cols[3]
        self.cols_show = [True]*len(self.cols)
        self.cols_show[2] = False
        self.cols_len = [30, 12, 12, 12, 12]

    def inc_duable(self, inc=1):
        if not self.duable or not self.duables:
            return
        newi = (self.duables.index(self.duable)+inc)%(len(self.duables))
        self.duable = self.duables[newi]

    def inc_view(self, inc=1):
        if not self.view or not self.views:
            return
        newi = (self.views.index(self.view)+inc)%(len(self.views)) 
        self.view = self.views[newi]

    def inc_vcols(self, inc=1):
        vcols = self.vcols()
        if not self.col or not vcols:
            return
        newi = (vcols.index(self.col)+inc)%(len(vcols))
        self.col = vcols[newi]
            
    def vcols(self):
        """
        Return list of v(isible) col(umn)s
        """
        return [col for col,show in zip(self.cols,self.cols_show) if show]

    def _process_query(self, query):
        """
        Put the results of the query into the interface.
        """
        self.duables = [duable for duable in query]
        if self.duable not in self.duables:
            if self.duables:
                self.duable = self.duables[0]

    def _base_query(self):
        query = self.session.query(Duable).order_by(self.col)
        if not self.show_done:
            query = query.filter(Duable.done == False)
        if not self.show_all_post:
            query = query.filter(Duable.post < datetime.now())
        return query

    def query(self):
        self._process_query(self.view.filter(self._base_query()))
