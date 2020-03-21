from flask import Markup
import io
from typing import List, Tuple
from PIL import Image, ImageDraw
import config


def showPNGBad(grid):

    import matplotlib.pyplot as plt

    """Generate a simple image of the maze."""
    plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation="nearest")
    plt.xticks([]), plt.yticks([])
    plt.save_fig(format="png")


def render_image(grid: List[List], start: Tuple, end: Tuple) -> io.BytesIO:
    """
    Take in maze grid, start and end locations and render an imaage

    Args:
        grid:
        start:
        end:

    Returns:

    """

    row_max = len(grid)
    col_max = len(grid[0])

    buf = io.BytesIO()

    img = Image.new("RGB", (row_max, col_max), "white")  # Create a new black image
    pixels = img.load()  # Create the pixel map
    for row in range(row_max):
        for col in range(col_max):
            if (row, col) == start:
                pixels[row, col] = (row, col, 2)
            elif (row, col) == end:
                pixels[row, col] = (row, col, 100)
            elif grid[row][col]:
                pixels[row, col] = (row, col, 255)

    img = img.resize(
        (config.default_image_size[0] * config.default_image_dpi,
        config.default_image_size[1] * config.default_image_dpi),
        Image.NEAREST
    )
    img.save(buf, "PNG")
    buf.seek(0)
    return buf


def showPNG_old(grid, start, end):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    import matplotlib.figure
    from matplotlib.figure import Figure
    import matplotlib.patches as patches

    fig = Figure(figsize=(9, 11), dpi=150)
    canvas = FigureCanvas(fig)
    ax = fig.add_axes(
        [0.05, 0.05, 0.9, 0.9]
    )  # [left, bottom, width, height] in fractions of width/height
    print(f"{start} to {end}")
    ax.imshow(grid, interpolation="nearest")

    ax.annotate("end", (20, 26))
    ax.annotate("start", (2, 2))
    ax.set_xticks([])
    ax.set_yticks([])
    fig.suptitle("www. Make A Maze .com")

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf.read()


def toHTML(grid, start, end, cell_size=20):

    row_max = len(grid)
    col_max = len(grid[0])

    print(start)
    print(end)

    html_css = Markup(
        '<style type="text/css">'
        + "#maze {width: "
        + str(cell_size * col_max)
        + "px;height: "
        + str(cell_size * row_max)
        + "px;border: 3px solid grey;}"
        + "div.maze_row div{width: "
        + str(cell_size)
        + "px;height: "
        + str(cell_size)
        + "px;}"
        + "div.maze_row div.bl{background-color: black; }"
        + "div.maze_row div.wh{background-color: white;}"
        + "div.maze_row div.rd{background-color: red;}"
        + "div.maze_row div.gr{background-color: green;}"
        + "div.maze_row div{float: left; }"
        + 'div.maze_row:after{content: ".";height: 0;visibility: hidden;display: block;clear: both;}'
        + "</style>"
    )

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
        html += "</div>"
    html += "</div>"

    return Markup(html), html_css
