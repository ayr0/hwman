import curses
from datetime import datetime
from .models import Duable, Course, Session
from .datetimehelp import get_datetime

class Painter(object):
    """
    This class uses ncurses to display the information in a Navigator, and
    provide updates to it from user input.
    """

    def __init__(self, navigator):
        """
        Create a painter.

        Parameters
        ----------
        navigator : hwman.Navigator
            The instantiated Navigator. This will already be connected to the
            database.
        """
        self.nav = navigator
        self.message = ''
        self.quit = False

        
    def run(self):
        curses.wrapper(self._run)

    def _run(self, stdscr):
        curses.curs_set(0)
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_MAGENTA, -1)
        self.nav.query()
        self.paint(stdscr)
        while not self.quit:
            self.input(stdscr)
            self.paint(stdscr)

    def input(self, scr):
        ch = scr.getch()
        if ch == ord('q'):
            self.quit = True
        elif ch == ord('j'):
            self.nav.inc_duable()
        elif ch == ord('k'): 
            self.nav.inc_duable(-1)
        elif ch == ord('l'): 
            self.nav.inc_view()
            self.nav.query()
        elif ch == ord('h'): 
            self.nav.inc_view(-1)
            self.nav.query()
        elif ch == ord('o'):
            self.nav.inc_order_bys()
            self.nav.query()
        elif ch == ord('O'):
            self.nav.inc_order_bys(-1)
            self.nav.query()
        elif ch == ord('e'):
            for item in self.nav.view.items():
                new = self.get_str(scr, '{} : '.format(item[0])) 
                if new:
                    self.nav.view[item[0]] = new
                    self.nav.query()
        elif ch == ord('x'):
            self.nav.duable.done = not self.nav.duable.done
        elif ch == ord('D'):
            self.nav.show_done = not self.nav.show_done
            self.nav.query()
        elif ch == ord('N'):
            new = Duable('new')
            new.done = False
            self.nav.session.add(new)
            self.nav.duable = new
            self.nav.view = self.nav.views[0]
            self.nav.query()
        elif ch == ord('S'):
            self.nav.session.commit()
            self.message = 'Saved.'
        elif ch == ord('R'):
            self.nav.session.rollback()
            self.nav.query()
            self.message = 'Rolled back.'
        elif ch == ord('X'):
            to_delete = self.nav.duable
            self.nav.inc_duable()
            self.nav.session.delete(to_delete)
            self.nav.query()
        elif ch == ord('n'):
            new_name = self.get_str(scr, 'name : ')
            if new_name:
                self.nav.duable.name = new_name
        elif ch == ord('t'):
            new_type = self.get_str(scr, 'type : ')
            if new_type:
                self.nav.duable.type = new_type
        elif ch == ord('d'):
            new_due = self.get_str(scr, 'due : ')
            if new_due:
                try:
                    new_due = get_datetime(new_due)
                    self.nav.duable.due = new_due
                except ValueError as e:
                    self.message = str(e)
        elif ch == ord('c'):
            new_course = self.get_str(scr, 'course : ')
            try:
                new_course = self.nav.session.query(Course).filter(
                              Course.course == new_course).one()
                self.nav.duable.course = new_course
            except Exception as e:
                self.message = e.__repr__()
            except BaseException as e:
                self.message = e.__repr__()
        else:
            pass

    def paint(self, scr):
        scr.clear()
        scr.move(0,0)

        #views
        scr.addstr('Views:')
        for view in self.nav.views:
            style = 0
            if view is self.nav.view:
                style += curses.A_REVERSE
            scr.addstr(' ')
            scr.addstr('{}'.format(view.name), style)
        scr.addstr('\n\n')

        #order_by
        scr.addstr('order by : {}'.format(self.nav.order_by))
        scr.addstr('\n\n')


        #view items
        for item in self.nav.view.items():
                scr.addstr('{} : {}  '.format(item[0],item[1]))
        scr.addstr('\n\n')

        #description
        scr.addstr('description : {}'.format(self.nav.duable.description))
        scr.addstr('\n\n')

        #duable table
        row = '  {:<20} {:<10} {:<10} {:<10}\n'
        scr.addstr(row.format('name','type','due','course'))
        scr.addstr(row.format('----','----','---','------'))
        if self.nav.duables:
            for duable in self.nav.duables:
                style = 0
                if duable.done:
                    style += curses.color_pair(1)
                elif duable.done is None:
                    style += curses.color_pair(2)
                if duable is self.nav.duable:
                    style += curses.A_REVERSE
                
                if duable.name:
                    name = duable.name[:20]
                else:
                    name = '<none>'
                if duable.type:
                    type_ = duable.type[:10]
                else:
                    type_ = '<none>'
                if type(duable.due) is datetime:
                    fdate = datetime.strftime(duable.due, '%d-%b-%y')
                elif duable.due:
                    fdate = duable.due[:10]
                else:
                    fdate = '<none>'
                if duable.course and duable.course.course:
                    course = duable.course.course[:10]
                else:
                    course = '<none>'

                scr.addstr(row.format(name, 
                           type_,
                           fdate,
                           course,
                           ), style)

        #message
        y = scr.getmaxyx()[0]-1
        scr.move(y, 0)
        scr.addstr(self.message)

        scr.refresh()

    def get_str(self, scr, query=''):
        s = None
        curses.echo()
        try:
            y = scr.getmaxyx()[0]-3
            scr.move(y, 0)
            scr.addstr(query)
            s = scr.getstr(y, len(query)+1)
        except KeyboardInterrupt:
            s = None
        finally:
            curses.noecho()
        return s
