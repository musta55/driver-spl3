from py2cfg import CFGBuilder
import pydot

cfg = CFGBuilder().build_from_file('Fibonacci', './Fibonacci.py')
cfg.build_visual('exampleCFG', 'png')
