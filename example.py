# Visualization Source Code
# =========================
# Use 1, 2, 3, 4, 5 keys to select different control points.
# Use h, j, k, l to move the points around and observe the changes in the spline.

from os import system
import bashdraw as bd
import keyboard

g = bd.Display(21, 21, bd.LEFT)
g.NewState('A')
g.SetState('A')
# g.DrawFigure(bd.Rectangle(0, 0, 21, 21, 'blue'))
# g.DrawFigure(bd.Line(1, 1, 19, 19, 'cyan'))
# g.DrawFigure(bd.Line(19, 1, 1, 19, 'cyan'))
# g.DrawFigure(bd.Line(10, 1, 10, 19, 'cyan'))
# g.DrawFigure(bd.Line(1, 10, 19, 10, 'cyan'))
# g.DrawFigure(bd.Line(5, 1, 15, 19, 'cyan'))
# g.DrawFigure(bd.Line(15, 1, 5, 19, 'cyan'))
# g.DrawFigure(bd.Line(1, 5, 19, 15, 'cyan'))
# g.DrawFigure(bd.Line(1, 15, 19, 5, 'cyan'))
# g.DrawFigure(bd.Rectangle(9, 9, 3, 3, 'white'))

# g.DrawFigure(bd.Triangle(4, 4, 16, 8, 8, 16, True, 'red'))
def addX(val, num):
    global g
    if not ((val.X == 0 and num == -1) or (val.X == g.dim.W - 1 and num == 1)):
        val.X += num
    redraw()
    return True
def addY(val, num):
    global g
    if not ((val.Y == 0 and num == -1) or (val.Y == g.dim.H - 1 and num == 1)):
        val.Y += num
    redraw()
    return True
def setsel(val):
    global sel, p
    p[sel] = bd.Point(p[sel].X, p[sel].Y, 'cyan')
    sel = val
    p[sel] = bd.Point(p[sel].X, p[sel].Y, 'yellow')
    redraw()
    return True
p = [bd.Point(1, 1, 'yellow'), bd.Point(8, 20, 'cyan'), bd.Point(12, 3, 'cyan'), bd.Point(15, 15, 'cyan'), bd.Point(18, 18, 'cyan')]
sel = 0
keyboard.add_hotkey('1', lambda: setsel(0))
keyboard.add_hotkey('2', lambda: setsel(1))
keyboard.add_hotkey('3', lambda: setsel(2))
keyboard.add_hotkey('4', lambda: setsel(3))
keyboard.add_hotkey('5', lambda: setsel(4))
keyboard.add_hotkey('h', lambda: addX(p[sel], -1))
keyboard.add_hotkey('j', lambda: addY(p[sel], 1))
keyboard.add_hotkey('k', lambda: addY(p[sel], -1))
keyboard.add_hotkey('l', lambda: addX(p[sel], 1))
def redraw():
    g.Clear()
    g.DrawFigure(bd.Rectangle(0, 0, g.dim.W, g.dim.H, 'grey'))
    g.DrawFigure(bd.Spline(bd.Spline.CATMULL_ROM, p[0], p[1], p[2], p[3], 'red'))
    g.DrawFigure(p[0])
    g.DrawFigure(p[1])
    g.DrawFigure(p[2])
    g.DrawFigure(p[3])
    g.DrawFigure(p[4])
    system('clear')
    g.Draw()
redraw()
while True:
    pass
