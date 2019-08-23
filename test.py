import bashdraw as bd

g = bd.Display(10, 10)
g.NewState('A')
g.SetState('A')
g.DrawFigure(bd.Rectangle(0, 0, 10, 10, 'white'))
g.DrawFigure(bd.Line(2, 8, 4, 1, 'violet'))
g.Draw()
