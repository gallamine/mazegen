from flask import Markup
import io

def showPNGBad(grid):

    import matplotlib.pyplot as plt

    """Generate a simple image of the maze."""
    plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.save_fig(format="png")


def showPNG(grid, start, end):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    import matplotlib.figure
    from matplotlib.figure import Figure
    import matplotlib.patches as patches

    fig = Figure(figsize=(9, 11), dpi=150)
    canvas = FigureCanvas(fig)
    ax = fig.add_axes([0.05, 0.05, .9, .9])         # [left, bottom, width, height] in fractions of width/height
    print(f"{start} to {end}")
    ax.imshow(grid, interpolation='nearest')

    ax.annotate("end", (20,26))
    ax.annotate("start", (2,2))
    ax.set_xticks([])
    ax.set_yticks([])
    fig.suptitle("www. Make A Maze .com")

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf.read()


def toHTML(grid, start, end, cell_size=20):

    row_max = len(grid)
    col_max = len(grid[0])

    print(start)
    print(end)


    html_css = Markup('<style type="text/css">' + \
           '#maze {width: ' + str(cell_size * col_max) + 'px;height: ' + \
           str(cell_size * row_max) + 'px;border: 3px solid grey;}' + \
           'div.maze_row div{width: ' + str(cell_size) + 'px;height: ' + str(cell_size) + 'px;}' + \
           'div.maze_row div.bl{background-color: black; }' + \
           'div.maze_row div.wh{background-color: white;}' + \
           'div.maze_row div.rd{background-color: red;}' + \
           'div.maze_row div.gr{background-color: green;}' + \
           'div.maze_row div{float: left; }' + \
           'div.maze_row:after{content: ".";height: 0;visibility: hidden;display: block;clear: both;}' + \
           '</style>')

    html = ""
    for row in range(row_max):
        html += '<div class="maze_row">'
        for col in range(col_max):
            if (row, col) == start:
                html += '<div class="gr"></div>'
            elif (row, col) == end:
                html += '<div class="rd"></div>'
            elif grid[row][col]:
                html += '<div class="bl"></div>'
            else:
                html += '<div class="wh"></div>'
        html += '</div>'
    html += '</div>'

    return Markup(html), html_css