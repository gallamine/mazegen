from flask import Flask
from flask import request, render_template, make_response
from app.mazegen import Maze
import maze_display as md
from mazelib import *

app = Flask(__name__)

@app.route("/")
def hello():
	width = request.args.get('width', default = 20, type = int)
	height = request.args.get('height', default = 26, type = int)
	difficulty = request.args.get('difficulty', default=1.0, type =float)


	m = Maze()
	m.generator = BacktrackingGenerator(height, width)
	m.solver = WallFollower()
	m.generate_monte_carlo(10, 10, difficulty)

	return md.toHTML(m.grid, m.start, m.end)

@app.route("/pdf")
def pdf_maze():

	from fpdf import FPDF

	width = request.args.get('width', default = 12, type = int)
	height = request.args.get('height', default = 12, type = int)
	m = Maze.generate(width, height)

	pdf = FPDF()
	pdf.add_page()
	pdf.set_font('Arial', 'B', 16, uni=True)
	pdf.cell(40, 10, str(m))
	pdf.output('tuto1.pdf', 'F')
	with open('tuto1.pdf', 'rb') as f:
		response = make_response(f.read())
		response.headers['Content-Type'] = 'application/pdf'
		response.headers['Content-Disposition'] = \
			'inline; filename=%s.pdf' % 'yourfilename'
		return response