import curses
from datetime import datetime

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
        else:
            pass

    def paint(self, scr):
        scr.clear()
        scr.move(0,0)
        scr.addstr('Views:')
        for view in self.nav.views:
            if view is self.nav.view:
                scr.addstr(' ')
                scr.addstr('{}'.format(view.name), curses.A_REVERSE)
            else:
                scr.addstr(' {}'.format(view.name))
        scr.addstr('\n\n')

        scr.addstr('order by : {}'.format(self.nav.order_by))
        scr.addstr('\n\n')
        
        for item in self.nav.view.items():
                scr.addstr('{} : {}  '.format(item[0],item[1]))
        scr.addstr('\n\n')

        scr.addstr('  {:<20} {:<10}\n'.format('name','due'))
        scr.addstr('  {:<20} {:<10}\n'.format('----','---'))
        if self.nav.duables:
            for duable in self.nav.duables:
                if type(duable.date_due) is datetime:
                    fdate = datetime.strftime(duable.date_due, '%d-%b-%y')
                else:
                    fdate = duable.date_due
                if duable is self.nav.duable:
                    scr.addstr('  {:<20} {:<10}\n'.format(duable.name, fdate),
                                       curses.A_REVERSE,)
                else:
                    scr.addstr('  {:<20} {:<10}\n'.format(duable.name, fdate))
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
