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
        self._slice_start = 0
        
    def run(self):
        curses.wrapper(self._run)

    def _run(self, stdscr):
        curses.curs_set(0)
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_MAGENTA, -1)
        curses.init_pair(3, curses.COLOR_CYAN, -1)
        self.nav.query()
        self.paint(stdscr)
        while not self.quit:
            self.input(stdscr)
            self.paint(stdscr)

    def input(self, scr):
        self.message = ''
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
            self.nav.inc_vcols()
            self.nav.query()
        elif ch == ord('O'):
            self.nav.inc_vcols(-1)
            self.nav.query()
        elif ch == ord('e'):
            for item in self.nav.view.items():
                new = self.get_str(scr, '{} : '.format(item[0])) 
                if new:
                    self.nav.view[item[0]] = new
                    self.nav.query()
        elif ch == ord('x'):
            self.nav.duable.done = not self.nav.duable.done
            self.nav.query()
        elif ch == ord('D'):
            self.nav.show_done = not self.nav.show_done
            self.nav.query()
        elif ch == ord('P'):
            self.nav.show_all_post = not self.nav.show_all_post
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
                self.nav.query()
        elif ch == ord('t'):
            new_type = self.get_str(scr, 'type : ')
            if new_type:
                self.nav.duable.type = new_type
                self.nav.query()
        elif ch == ord('p'):
            new_post = self.get_str(scr, 'post : ')
            if new_post:
                try:
                    new_post= get_datetime(new_post)
                    self.nav.duable.post = new_post
                    self.nav.query()
                except ValueError as e:
                    self.message = str(e)
        elif ch == ord('d'):
            new_due = self.get_str(scr, 'due : ')
            if new_due:
                try:
                    new_due = get_datetime(new_due)
                    self.nav.duable.due = new_due
                    self.nav.query()
                except ValueError as e:
                    self.message = str(e)
        elif ch == ord('c'):
            new_course = self.get_str(scr, 'course : ')
            try:
                new_course = self.nav.session.query(Course).filter(
                              Course.course == new_course).one()
                self.nav.duable.course = new_course
                self.nav.query()
            except Exception as e:
                self.message = e.__repr__()
            except BaseException as e:
                self.message = e.__repr__()
        elif ch == ord('s'):
            new_desc = self.get_str(scr, 'description : ')
            if new_desc:
                self.nav.duable.description = new_desc
                self.nav.query()
        elif ch == ord('1'):
            if not self.nav.cols_show[0]:
                self.nav.col = self.nav.cols[0]
            elif self.nav.col is self.nav.cols[0]:
                self.nav.inc_vcols()
            self.nav.cols_show[0] = not self.nav.cols_show[0]
        elif ch == ord('2'):
            if not self.nav.cols_show[1]:
                self.nav.col = self.nav.cols[1]
            elif self.nav.col is self.nav.cols[1]:
                self.nav.inc_vcols()
            self.nav.cols_show[1] = not self.nav.cols_show[1]
        elif ch == ord('3'):
            if not self.nav.cols_show[2]:
                self.nav.col = self.nav.cols[2]
            elif self.nav.col is self.nav.cols[2]:
                self.nav.inc_vcols()
            self.nav.cols_show[2] = not self.nav.cols_show[2]
        elif ch == ord('4'):
            if not self.nav.cols_show[3]:
                self.nav.col = self.nav.cols[3]
            elif self.nav.col is self.nav.cols[3]:
                self.nav.inc_vcols()
            self.nav.cols_show[3] = not self.nav.cols_show[3]
        elif ch == ord('5'):
            if not self.nav.cols_show[4]:
                self.nav.col = self.nav.cols[4]
            elif self.nav.col is self.nav.cols[4]:
                self.nav.inc_vcols()
            self.nav.cols_show[4] = not self.nav.cols_show[4]
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

            #nums
        scr.addstr(' ')
        for bool_,col_num in zip(self.nav.cols_show,range(1,
                                 len(self.nav.cols_show)+1)):
            style = 0
            if bool_:
                style += curses.color_pair(3)
            scr.addstr('{}'.format(col_num),style)
    
            #bools
        style = 0
        if self.nav.show_done:
            style += curses.color_pair(3)
        scr.addstr(' DONE',style)
        style = 0
        if self.nav.show_all_post:
            style += curses.color_pair(3)
        scr.addstr(' POST',style)

        scr.addstr('\n')

        #view items
        for item in self.nav.view.items():
                scr.addstr('{} : {}  '.format(item[0],item[1]))
        scr.addstr('\n')

        if self.nav.duable and any(self.nav.cols_show):
            #description
            if self.nav.duable.description:
                desc = self.nav.duable.description
            else:
                desc = '<none>'
            if self.nav.duable.name:
                name = self.nav.duable.name
            else:
                name = '<none>'
            scr.addstr('name : {}\n'.format(name))
            scr.addstr('description : {}\n\n'.format(desc))

            #duable table
            vcols = self.nav.vcols()
            names = [col.property.key for col in vcols]
            row = ('  ' + '{{{{{{}}:<{}}}}}'*len(vcols) + '\n').format(*self.nav.cols_len).format(*names)
            #bars = ['-'*len(name) for name in names]
            scr.addstr('  ')
            for col,len_ in zip(vcols,self.nav.cols_len):
                style = 0
                if col is self.nav.col:
                    style += curses.color_pair(3)
                scr.addstr('{{:<{}}}'.format(len_).format(col.property.key),style)
            scr.addstr('\n')
            #scr.addstr(row.format(*bars))
            if self.nav.duables:
                self._make_slice(scr)
                for duable in self.nav.duables[self._slice_start:self._slice_end]:
                    style = 0
                    if duable.done:
                        style += curses.color_pair(1)
                    elif duable.done is None:
                        style += curses.color_pair(2)
                    if duable is self.nav.duable:
                        style += curses.A_REVERSE
                    
                    if duable.name:
                        name = duable.name[:self.nav.cols_len[0]-1]
                    else:
                        name = '<none>'
                    if duable.type:
                        type_ = duable.type[:10]
                    else:
                        type_ = '<none>'
                    if type(duable.due) is datetime:
                        fdue = datetime.strftime(duable.due, '%d-%b-%y')
                    elif duable.due:
                        fdue = duable.due[:10]
                    else:
                        fdue = '<none>'
                    if type(duable.post) is datetime:
                        fpost = datetime.strftime(duable.post, '%d-%b-%y')
                    elif duable.post:
                        fpost = duable.post[:10]
                    else:
                        fpost = '<none>'
                    if duable.course and duable.course.course:
                        course = duable.course.course[:10]
                    else:
                        course = '<none>'
                    scr.addstr(row.format(name=name, 
                               type=type_,
                               post=fpost, 
                               due=fdue,
                               course=course,
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

    def _make_slice(self, scr, ignore=9):
        """
        Determine which section of the list to display.
        """
        self._slice_len = min(scr.getmaxyx()[0]-ignore,len(self.nav.duables))
        di = self.nav.duables.index(self.nav.duable)
        while di - self._slice_start < 2:
            if self._slice_start == 0:
                break
            self._slice_start -= 1
        self._slice_end = self._slice_start + self._slice_len
        while self._slice_end - 1 - di < 2:
            if self._slice_end == len(self.nav.duables):
                break
            self._slice_start += 1
            self._slice_end = self._slice_start + self._slice_len
