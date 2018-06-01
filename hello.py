from flask import Flask
from flask import request, render_template
from app.mazegen import Maze

app = Flask(__name__)

@app.route("/")
def hello():
	width = request.args.get('width', default = 12, type = int)
	height = request.args.get('height', default = 12, type = int)
	m = Maze.generate(width, height)
	return render_template('index.html', maze_repr=str(m))