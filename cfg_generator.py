from py2cfg import CFGBuilder
import pydot

cfg = CFGBuilder().build_from_file('Fibonacci', './lcs.py')
cfg.build_visual('exampleCFG', 'png')

def dot_to_svg(dot_file, svg_file):
  """Converts a DOT file to an SVG file.

  Args:
    dot_file: The path to the DOT file.
    svg_file: The path to the output SVG file.
  """

  graph = pydot.graph_from_dot_file(dot_file)
  svg_string = graph[0].write_png(svg_file)

#   with open(svg_file, "w") as f:
#     f.write(svg_string)

# Example usage:

dot_file = "Fibonacci"
svg_file = "Fibonacci.svg"

dot_to_svg(dot_file, svg_file)