from .models import Duable, Course
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

class View(dict):
    """
    A view is a filter on all Duables, and can be parameter based. All
    parameters of the view, and only they, are to be keys.
    """
    def __init__(self):
        self.name = None
        pass
        
    def filter(self, query):
        raise NotImplementedError()

    def __repr__(self):
        return '<View {}({})>'.format(self.name, super(View,self).__repr__())

class View_all(View):
    def __init__(self):
        """
        Populate all duables.
        """
        self.name = 'all'
        pass

    def filter(self, query):
        return query

    def __bool__(self):
        return True
    __nonzero__ = __bool__


class View_due(View):
    def __init__(self, within='3 days'): 
        """
        Populate duables within due parameters.
        """
        self.name = 'due'
        self['within'] = within

    def filter(self, query):
        vals = self['within'].split()
        param = {vals[1] : int(vals[0])}
        threshold = dt.now() + relativedelta(**param)
        return query.filter(Duable.due < threshold)

class View_name(View):
    def __init__(self, like='%'):
        """
        Populate duables with name like the parameter.
        """
        self.name = 'name'
        self['like'] = like

    def filter(self, query):
        return query.filter(Duable.name.like(self['like']))

class View_course(View):
    def __init__(self, course=''):
        """
        Populate duables whose course has the specified value in field.
        """
        self.name = 'course'
        self['course'] = course

    def filter(self, query):
        _query = query.filter(Duable.course.has(
                            course=self['course']))
        if not _query.first(): 
            _query = query.join(Course).filter(Course.course_title.like(
                                   '%{}%'.format(self['course'])))
        return _query
