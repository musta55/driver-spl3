from py2cfg import CFGBuilder
import pydot

cfg = CFGBuilder().build_from_file('Fibonacci', './Fibonacci.py')
cfg.build_visual('exampleCFG', 'png')

def dot_to_svg(dot_file, svg_file):

  graph = pydot.graph_from_dot_file(dot_file)
  svg_string = graph[0].write_png(svg_file)


dot_file = "Fibonacci"
svg_file = "Fibonacci.svg"

dot_to_svg(dot_file, svg_file)