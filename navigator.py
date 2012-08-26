from .models import Duable
from datetime import datetime as dt

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

    def _process_query(self, query):
        self.duables = [duable for duable in query]
        if self.duable not in self.duables:
            if self.duables:
                self.duable = self.duables[0]
            else:
                self.duable = None

    def query_all(self):
        """
        Populate all duables.
        """
        query = self.session.query(Duable).order_by(self.order_by)
        self._process_query(query) 

    def query_due(self, within=(3,'days')):
        """
        Populate duables within due parameters.
        """
        query = self.session.query(Duable).order_by(self.order_by).filter(
                 getattr(Duable.date_due-dt.now(),within[1]) < within[0])
        self._process_query(query)

        

