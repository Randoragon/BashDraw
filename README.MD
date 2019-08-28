# BashPython

All modules are written in Python 3.7. They are not available via PyPi or anything alike, you have to download the python file and import it from your working directory.

## BashDraw Module

This module lets you define a rectangular canvas inside a command line environment, and draw basic shapes in various colors inside it.

### Example 1

```python
import bashdraw as bd

d = bd.Display(25, 25)  # Initialize a 25x25 pixels display
d.NewState('MyState')   # You need at least 1 state to be able to draw, use any object as identifier
d.SetState('MyState')   # Set the working state to 'MyState'
d.Clear('MyState')      # This resets the entire 'MyState' canvas to pitch black. Omit the state parameter to use the last set state.

f1 = bd.Point(0, 0, 'white')    # Create a Point figure at coordinates 0, 0 and white color
d.DrawFigure(f1)                # Draw the point to the display.
d.DrawFigure(f1, 'MyState')     # This line and above are identical in this context, if no state parameter is specified, the last set state is used implicitly
d.Draw()                        # Draw the current state to the terminal.
```

Here's the output of the above code:

![Imgur](https://imgur.com/m9Fd6xy)

### Documentation

#### Available Figures (v1.0.0)

1. Point(x, y, color = 'white')
2. Rectangle(x0, y0, width, height, fill = False, color = 'white') **OR** Rectangle.FromPoints(p0, p1, fill = False, color = 'white')
3. Line(x0, y0, x1, y1, color = 'white') **OR** Line.FromPoints(p0, p1, color = 'white')
4. Triangle(x0, y0, x1, y1, x2, y2, fill = True, color = 'white') **OR** Triangle.FromPoints(p0, p1, p2, fill = True, color = 'white')
4. Chain(p0, p1, ..., pn, color = 'white') - this draws a serie of connected Lines
5. Spline(p0, p1, ..., pn, color = 'white') - this draws a Bézier curve

- ``x, y`` parameters refer to integer x and y position of the display.
- ``p0, p1`` parameters refer to Point objects.

#### Horizontal Alignment

You can control where the display will be drawn by passing an optional align parameter:

```python
import bashdraw as bd

d = bd.Display(10, 10, bd.LEFT)     # This is the default setting
d = bd.Display(10, 10, bd.CENTER)
d = bd.Display(10, 10, bd.RIGHT)
```

### Example 2

```python
import bashdraw as bd

d = bd.Display(20, 20, bd.CENTER)
d.NewState(0)
d.SetState(0)

d.DrawFigure(bd.Rectangle(0, 0, 20, 20, 'yellow', True))
d.DrawFigure(bd.Spline(bd.Point(4, 14), bd.Point(7, 16), bd.Point(13, 15), bd.Point(16, 11), 'red'))
d.DrawFigure(bd.Line(6, 5, 6, 7, 'cyan'))
d.DrawFigure(bd.Line(13, 5, 13, 7, 'cyan'))

d.Draw()
```

This gives the following output:

![Imgur](https://imgur.com/UwwWJRc)
