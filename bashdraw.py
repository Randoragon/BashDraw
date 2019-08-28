from termcolor import cprint
from math import floor, ceil
from Color_Console import ctext
from terminalsize import get_terminal_size

LEFT = 0
CENTER = 1
RIGHT = 2


def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0

def WhichLineSide(x, y, x0, y0, x1, y1):
    det = x*y0 + y*x1 + x0*y1 - x1*y0 - y1*x - x0*y
    return sign(det)

colors = [
        'black',
        'grey',
        'red',
        'green',
        'yellow',
        'blue',
        'magenta',
        'cyan',
        'white'
        ]

if __name__ == '__main__':
    print('This is a module!')

ctext('') # For some reason colors in windows terminal don't work until I've called ctext() at least once, so here it is, unfortunately

class Figure:
    def __init__(self, color = 'white'):
        if color not in colors:
            raise ValueError('\'color\' must be one of these values: \'white\', \'red\', \'green\', \'blue\', \'yellow\', \'magenta\', \'cyan\', \'grey\', \'black\'.')
        self.color = color
class Rectangle(Figure):
    def __init__(self, x, y, w, h, color = 'white', fill = False):
        Figure.__init__(self, color)
        self.X = x
        self.Y = y
        self.W = w
        self.H = h
        self.fill = fill
    @classmethod
    def FromPoints(cls, a, b, color = 'white', fill = False):
        return cls(a.X, b.X, b.X - a.X, b.Y - a.Y, color, fill)
class Point(Figure):
    def __init__(self, x, y, color = 'white'):
        Figure.__init__(self, color)
        self.X = x
        self.Y = y
    def __repr__(self):
        return 'Point{}'.format(self.__str__())
    def __str__(self):
        return str((self.X, self.Y))
    def __getitem__(self, key):
        return self.X if key == 0 else self.Y

class Line(Figure):
    def __init__(self, x0, y0, x1, y1, color = 'white'):
        Figure.__init__(self, color)
        if x0 != x1:
            self.slope = Line.Slope(x0, y0, x1, y1)
            if self.slope <= 1 and self.slope >= -1:
                if x0 < x1:
                    self.X0 = x0
                    self.Y0 = y0
                    self.X1 = x1
                    self.Y1 = y1
                elif x1 < x0:
                    self.X1 = x0
                    self.Y1 = y0
                    self.X0 = x1
                    self.Y0 = y1
                else:
                    raise ValueError('The described line begins and ends in the same spot. Please use a Point instead.')
            else:
                if y0 < y1:
                    self.X0 = x0
                    self.Y0 = y0
                    self.X1 = x1
                    self.Y1 = y1
                elif y1 < y0:
                    self.X1 = x0
                    self.Y1 = y0
                    self.X0 = x1
                    self.Y0 = y1
                else:
                    raise ValueError('The described line begins and ends in the same spot. Please use a Point instead.')
        else:
            self.slope = None
            if y0 <= y1:
                self.X0 = x0
                self.Y0 = y0
                self.X1 = x1
                self.Y1 = y1
            else:
                self.X0 = x0
                self.Y0 = y1
                self.X1 = x1
                self.Y1 = y0
       
    @classmethod
    def FromPoints(cls, a, b, color = 'white'):
        if a.X <= b.X:
            return cls(a.X, a.Y, b.X, b.Y, color)
        else:
            return cls(b.X, b.Y, a.X, a.Y, color)
    @staticmethod
    def Slope(x0, y0, x1, y1):
        return (y1 - y0) / (x1 - x0)

class Triangle(Figure):
    def __init__(self, x0, y0, x1, y1, x2, y2, color = 'white', fill = False):
        Figure.__init__(self, color)
        self.X0 = x0
        self.Y0 = y0
        self.X1 = x1
        self.Y1 = y1
        self.X2 = x2
        self.Y2 = y2
        self.fill = fill
    @classmethod
    def FromPoints(cls, a, b, c, fill = True, color = 'white'):
        return cls(a.X, a.Y, b.X, b.Y, c.X, c.Y, fill, color)
class Chain(Figure):
    def __init__(self, *args):
        if len(args) < 2:
            raise ValueError('At least 2 arguments must be passed: Point1 and Point2.')
        elif len(args) > 2 and isinstance(args[-1], str):
            Figure.__init__(self, args[-1])
            args = args[:-1]
        else:
            Figure.__init__(self, 'white')
        self.P = []
        for i in args:
            self.P.append(i)
    def __getitem__(self, key):
        return self.P[key]

class Spline(Chain):
    BEZIER = 0
    CATMULL_ROM = 1
    def __init__(self, stype, *args):
        if isinstance(stype, int):
            Chain.__init__(self, *args)
            self.stype = stype
        else:
            raise ValueError('The first parameter must be the spline type! (Spline.BEZIER or Spline.CATMULL_ROM)')

class Display:
    class Grid:
        def __init__(self, w, h, fill, values = None):
            if values != None and fill not in values:
                raise ValueError('\'fill\' must be included in \'values\'!')
            self.W = w
            self.H = h
            if values == None or isinstance(values, tuple):
                self.__values = values
            else:
                raise TypeError('\'values\' must be a tuple')
            if values != None:
                self._grid = []
                for i in range(h):
                    self._grid.append(w * [fill])
            else:
                self._grid = [] 
                for i in range(h):
                    self._grid.append(w * [None])
        def Get(self, x, y):
            return (self._grid[y][x],)[0] # tuple because this needs to be read-only
        def Set(self, x, y, val):
            if self.__values == None or val in self.__values:
                self._grid[y][x] = val
            else:
                raise TypeError('\'val\' must be a part of the \'values\' collection: {}'.format(self.__values))
        def __getitem__(self, key):
            return tuple(self._grid[key]) # tuple because this needs to be read-only
    def __init__(self, w, h, align = LEFT):
        cols, rows = get_terminal_size()
        if w * 2 > cols or h + 1 > rows:
            raise ValueError('The given width and height are too big. Please resize your terminal or stick to these dimensions: {}x{}.'.format(cols // 2, rows + 1))
        self.dim = Rectangle(0, 0, w, h)
        self.align = align
        self.grid = {}
        self.state = None
    def NewState(self, state, fill='black'):
        self.grid[state] = self.Grid(self.dim.W, self.dim.H, fill, tuple(colors))
    def SetState(self, state):
        if state in self.grid:
            self.state = state
        else:
            raise ValueError('No state \'{}\' found. Did you call \'NewState()\'?'.format(state))
    def GetStates(self):
        return [k for k,v in self.grid.items()]
    def DrawFigure(self, figure, state = None):
        if state == None and self.state == None:
            raise ValueError('Must specify \'state\' parameter if \'SetState()\' had not been invoked before.')
        elif state != None and state not in self.grid:
            raise ValueError('No state \'{}\' found. Did you call \'NewState()\'?'.format(state))
        elif state == None:
            state = self.state
        if not isinstance(figure, Figure):
            raise ValueError('\'figure\' must be an instance of a class derived from Figure!')
        if isinstance(figure, Point):
            self.grid[state].Set(figure.X, figure.Y, figure.color)
        elif isinstance(figure, Rectangle):
            if not figure.fill:
                for i in range(figure.X, figure.X + figure.W):
                    self.grid[state].Set(i, figure.Y, figure.color)
                    self.grid[state].Set(i, figure.Y + figure.H - 1, figure.color)
                for i in range(figure.Y + 1, figure.Y + figure.H - 1):
                    self.grid[state].Set(figure.X, i, figure.color)
                    self.grid[state].Set(figure.X + figure.W - 1, i, figure.color)
            else:
                for i in range(figure.X, figure.X + figure.W):
                    for j in range(figure.Y, figure.Y + figure.H):
                        self.grid[state].Set(i, j, figure.color) 
        elif isinstance(figure, Line):
            if figure.slope != None:
                if figure.slope <= 1 and figure.slope >= -1:
                    funcx = lambda x: figure.Y0 + (x * figure.slope)
                    for i in range(0, figure.X1 - figure.X0 + 1):
                        self.grid[state].Set(figure.X0 + i, round(funcx(i)), figure.color)
                else:
                    funcy = lambda x: figure.X0 + (x * Line.Slope(figure.Y0, figure.X0, figure.Y1, figure.X1))
                    for i in range(0, figure.Y1 - figure.Y0 + 1):
                        self.grid[state].Set(round(funcy(i)), figure.Y0 + i, figure.color)
            else:
                for i in range(figure.Y0, figure.Y1 + 1):
                    self.grid[state].Set(figure.X0, i, figure.color)
        elif isinstance(figure, Triangle):
            self.DrawFigure(Line(figure.X0, figure.Y0, figure.X1, figure.Y1, figure.color), state)
            self.DrawFigure(Line(figure.X1, figure.Y1, figure.X2, figure.Y2, figure.color), state)
            self.DrawFigure(Line(figure.X2, figure.Y2, figure.X0, figure.Y0, figure.color), state)
            if figure.fill:
                for y in range(min(figure.Y0, figure.Y1, figure.Y2), max(figure.Y0, figure.Y1, figure.Y2) + 1):
                    for x in range(min(figure.X0, figure.X1, figure.X2), max(figure.X0, figure.X1, figure.X2) + 1):
                        if WhichLineSide(x, y, figure.X0, figure.Y0, figure.X1, figure.Y1) == WhichLineSide(x, y, figure.X1, figure.Y1, figure.X2, figure.Y2) and WhichLineSide(x, y, figure.X1, figure.Y1, figure.X2, figure.Y2) == WhichLineSide(x, y, figure.X2, figure.Y2, figure.X0, figure.Y0):
                            self.grid[state].Set(x, y, figure.color)
        elif isinstance(figure, Chain):
            if not isinstance(figure, Spline):
                for i in range(1, len(figure.P)):
                    self.DrawFigure(Line(figure.P[i-1].X, figure.P[i-1].Y, figure.P[i].X, figure.P[i].Y, figure.color), state)
            else:
                # This function will erase the last drawn point if the last 3 points form an L shape (simple pixel-perfect algorithm)
                def computepixelperfect(curPoint, lastPoint, lastPoint2):
                    def samecoords(p1, p2):
                        return p1.X == p2.X and p1.Y == p2.Y
                    def adjacent(p1, p2):
                        if abs(p1.X - p2.X) == 1 and p1.Y == p2.Y:
                            return 1
                        elif abs(p1.Y - p2.Y) == 1 and p1.X == p2.X:
                            return 2
                        else:
                            return 0
                    if lastPoint != None and lastPoint2 != None and not samecoords(lastPoint, lastPoint2) and not samecoords(curPoint, lastPoint):
                        if adjacent(curPoint, lastPoint) + adjacent(lastPoint, lastPoint2) == 3:
                            self.DrawFigure(lastPoint, state)
                            lastPoint = None
                    if lastPoint == None or not samecoords(curPoint, lastPoint):
                        if lastPoint2 == None or (lastPoint != None and not samecoords(lastPoint2, lastPoint)):
                            lastPoint2 = lastPoint
                        lastPoint = Point(x, y, self.grid[state].Get(x, y))
                    return lastPoint, lastPoint2

                lastPoint = None
                lastPoint2 = None
                if figure.stype == Spline.BEZIER:
                    def interp(a, b, t):
                        return a + (b - a) * t
                    steps = self.dim.H * self.dim.W
                    for i in range(steps + 1):
                        i = i / steps
                        P = figure.P
                        while len(P) > 2:
                            P2 = []
                            for j in range(len(P) - 1):
                                x = interp(P[j].X, P[j+1].X, i)
                                y = interp(P[j].Y, P[j+1].Y, i)
                                P2.append(Point(x, y))
                            P = P2
                        x = round(interp(P[0].X, P[1].X, i))
                        y = round(interp(P[0].Y, P[1].Y, i))

                        lastPoint, lastPoint2 = computepixelperfect(Point(x, y), lastPoint, lastPoint2)
                        self.DrawFigure(Point(x, y, figure.color), state)
                elif figure.stype == Spline.CATMULL_ROM:
                    steps = self.dim.H * self.dim.W
                    for i in range(steps + 1):
                        i = i / steps

                        p1 = int(i) + 1
                        p2 = p1 + 1
                        p3 = p2 + 1
                        p0 = p1 - 1

                        ii = i * i
                        iii = ii * i

                        q1 = (-3 * ii) + (4  * i) - 1
                        q2 = (+9 * ii) - (10 * i)
                        q3 = (-9 * ii) + (8  * i) + 1
                        q4 = (+3 * ii) - (2  * i)

                        x = round(0.5 * ((figure.P[0].X * q1) + (figure.P[1].X * q2) + (figure.P[2].X * q3) + (figure.P[3].X * q4)))
                        y = round(0.5 * ((figure.P[0].Y * q1) + (figure.P[1].Y * q2) + (figure.P[2].Y * q3) + (figure.P[3].Y * q4)))

                        if x in range(0, self.dim.W) and y in range(0, self.dim.H):
                            lastPoint, lastPoint2 = computepixelperfect(Point(x, y), lastPoint, lastPoint2)
                            self.DrawFigure(Point(x, y, figure.color), state)
    def Draw(self, state = None):
        if state == None and self.state != None:
            for i in range(self.dim.H):
                if self.align == CENTER:
                    for j in range((get_terminal_size()[0] // 2 - self.dim.W) // 2):
                        print('  ', end='')
                elif self.align == RIGHT:
                    for j in range(get_terminal_size()[0] // 2 - self.dim.W):
                        print('  ', end='')
                for j in range(self.dim.W):
                    col = self.grid[self.state].Get(j, i)
                    if col != 'black':
                        cprint('  ', col, 'on_' + self.grid[self.state].Get(j, i), end='')
                    else:
                        print('  ', end='')
                print('')
        elif state != None:
            for i in range(self.dim.H):
                if self.align == CENTER:
                    for j in range((get_terminal_size()[0] // 2 - self.dim.W) // 2):
                        print('  ', end='')
                elif self.align == RIGHT:
                    for j in range(get_terminal_size()[0] // 2 - self.dim.W):
                        print('  ', end='')
                for j in range(self.dim.W):
                    col = self.grid[state].Get(j, i)
                    if col != 'black':
                        cprint('  ', col, 'on_' + self.grid[state].Get(j, i), end='')
                    else:
                        print('  ', end='')
                print('')
        else:
            raise ValueError('Must specify \'state\' parameter if \'SetState()\' had not been invoked before.')
    def Clear(self, state = None):
        if state == None and self.state != None:
            self.DrawFigure(Rectangle(0, 0, self.dim.W, self.dim.H, 'black', True))
        elif state != None:
            self.DrawFigure(Rectangle(0, 0, self.dim.W, self.dim.H, 'black', True), state)
        else:
            raise ValueError('Must specify \'state\' parameter if \'SetState()\' had not been invoked before.')
