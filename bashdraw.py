import subprocess
import bashcolor as bc
from math import floor, ceil

LEFT = 0
CENTER = 1
RIGHT = 2

def GetTerminalSize():
    return tuple(map(int, subprocess.check_output(['stty', 'size']).split()))

def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0

def WhichLineSide(x, y, x0, y0, x1, y1):
    det = x*y0 + y*x1 + x0*y1 - x1*y0 - y1*x - x0*y
    return sign(det)

if __name__ == '__main__':
    print('This is a module!')
class Figure:
    def __init__(self, color = 'black'):
        if color not in Display.color or color[1:] == 'bg':
            raise ValueError('\'color\' must be one of these values: \'white\', \'red\', \'green\', \'blue\', \'yellow\', \'violet\', \'beige\', \'gray\', \'black\'.')
        self.color = color
class Rectangle(Figure):
    def __init__(self, x, y, w, h, color = 'black', fill = False):
        Figure.__init__(self, color)
        self.X = x
        self.Y = y
        self.W = w
        self.H = h
        self.fill = fill
    @classmethod
    def FromPoints(cls, a, b, color = 'black', fill = False):
        return cls(a.X, b.X, b.X - a.X, b.Y - a.Y, color, fill)
class Point(Figure):
    def __init__(self, x, y, color = 'black'):
        Figure.__init__(self, color)
        self.X = x
        self.Y = y
    def __getitem__(self, key):
        return self.X if key == 0 else self.Y

class Line(Figure):
    def __init__(self, x0, y0, x1, y1, color = 'black'):
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
    def FromPoints(cls, a, b, color = 'black'):
        if a.X <= b.X:
            return cls(a.X, a.Y, b.X, b.Y, color)
        else:
            return cls(b.X, b.Y, a.X, a.Y, color)
    @staticmethod
    def Slope(x0, y0, x1, y1):
        return (y1 - y0) / (x1 - x0)

class Triangle(Figure):
    def __init__(self, x0, y0, x1, y1, x2, y2, fill = True, color = 'black'):
        Figure.__init__(self, color)
        self.X0 = x0
        self.Y0 = y0
        self.X1 = x1
        self.Y1 = y1
        self.X2 = x2
        self.Y2 = y2
        self.fill = fill
    @classmethod
    def FromPoints(cls, a, b, c, fill = True, color = 'black'):
        return cls(a.X, a.Y, b.X, b.Y, c.X, c.Y, fill, color)
class Chain(Figure):
    def __init__(self, *args):
        if len(args) < 2:
            raise ValueError('At least 2 arguments must be passed: Point1 and Point2.')
        elif len(args) > 2 and isinstance(args[-1], str):
            Figure.__init__(self, args[-1])
            args = args[:-1]
        else:
            Figure.__init__(self, 'black')
        self.P = []
        for i in args:
            self.P.append(i)
    def __getitem__(self, key):
        return self.P[key]

class Spline(Chain):
    pass

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
    color = {
        'white' : bc.Color.CWHITE,
        'red'   : bc.Color.CRED,
        'green' : bc.Color.CGREEN,
        'blue'  : bc.Color.CBLUE,
        'yellow': bc.Color.CYELLOW,
        'violet': bc.Color.CVIOLET,
        'beige' : bc.Color.CBEIGE,
        'gray'  : bc.Color.CGREY,
        'black' : bc.Color.CBLACK,
        'whitebg' : bc.Color.CWHITEBG,
        'redbg'   : bc.Color.CREDBG,
        'greenbg' : bc.Color.CGREENBG,
        'bluebg'  : bc.Color.CBLUEBG,
        'yellowbg': bc.Color.CYELLOWBG,
        'violetbg': bc.Color.CVIOLETBG,
        'beigebg' : bc.Color.CBEIGEBG,
        'graybg'  : bc.Color.CGREYBG,
        'blackbg' : bc.Color.CBLACKBG,
    }
    def __init__(self, w, h, align = LEFT):
        rows, cols = GetTerminalSize()
        if w * 2 > cols or h + 1 > rows:
            raise ValueError('The given width and height are too big. Please resize your terminal or stick to these dimensions: {}x{}.'.format(cols * 2, rows + 1))
        self.dim = Rectangle(0, 0, w, h)
        self.align = align
        self.grid = {}
        self.state = None
    def NewState(self, state, fill='black'):
        self.grid[state] = self.Grid(self.dim.W, self.dim.H, fill, tuple(k for k,v in self.color.items()))
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
            for i in range(1, len(figure.P)):
                self.DrawFigure(Line(figure.P[i-1].X, figure.P[i-1].Y, figure.P[i].X, figure.P[i].Y, figure.color))
    def Draw(self, state = None):
        if state == None and self.state != None:
            for i in range(self.dim.H):
                if self.align == CENTER:
                    for j in range((GetTerminalSize()[1] // 2 - self.dim.W) // 2):
                        bc.printbc('  ', self.color['black'], self.color['blackbg'], end = '')
                elif self.align == RIGHT:
                    for j in range(GetTerminalSize()[1] // 2 - self.dim.W):
                        bc.printbc('  ', self.color['black'], self.color['blackbg'], end= '')
                for j in range(self.dim.W):
                    bc.printbc('  ', self.color[self.grid[self.state].Get(j, i)], self.color[self.grid[self.state].Get(j, i) + 'bg'], end='')
                print('')
        elif state != None:
            for i in range(self.dim.H):
                for j in range(self.dim.W):
                    bc.printbc('  ', self.color[self.grid[state].Get(j, i)], self.color[self.grid[state].Get(j, i) + 'bg'], end='')
                print('')
        else:
            raise ValueError('Must specify \'state\' parameter if \'SetState()\' had not been invoked before.')

