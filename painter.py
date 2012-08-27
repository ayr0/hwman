import curses
from datetime import datetime
from .models import Duable

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
        self.quit = False

        
    def run(self):
        curses.wrapper(self._run)

    def _run(self, stdscr):
        curses.curs_set(0)
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)
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
            self.nav.session.add(new)
            self.nav.duable = new
            self.nav.view = self.nav.views[0]
            self.nav.query()
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
                if type(duable.date_due) is datetime:
                    fdate = datetime.strftime(duable.date_due, '%d-%b-%y')
                else:
                    fdate = duable.date_due
                style = 0
                if duable.done:
                    style += curses.color_pair(1)
                if duable is self.nav.duable:
                    style += curses.A_REVERSE
                scr.addstr(row.format(duable.name[:20], 
                           duable.type[:10],
                           fdate[:10],
                           duable.course.course[:10],
                           ), style)
        scr.refresh()

    def get_str(self, scr, query=''):
        s = None
        curses.echo()
        try:
            y = scr.getmaxyx()[0]-1
            scr.move(y, 0)
            scr.addstr(query)
            s = scr.getstr(y, len(query)+1)
        except KeyboardInterrupt:
            s = None
        finally:
            curses.noecho()
        return s
