"""
Command line of Coprof.
"""

import sys
import click
#from coprof import from_file, gprof, parse, write_back, default_output, compare, read, Graph
from coprof import *

@click.group()
def main_cli():
	"""−−−−−−−−−−−−−−−−−  COPROF  −−−−−−−−−−−−−−−−−

You are now using te command line interface of Coprof
a Python3 helper to compare profiling data, created at CERFACS (https://cerfacs.fr).

This is a python package currently installed in your python environment.
"""
	pass


@click.command()
@click.argument('inputs', nargs=-1, type=click.Path(exists=True))
@click.option('-o', '--output', help="output file for the json profile")
def json(inputs, output):
	"""Extract a json profile from gprof analysis.

	INPUTS can be a single analysis file: coprof json analysis.txt

	or a gmon file with its corresponding program: coprof json gmon.out program
	for the later your computer must have the gprof command installed
	"""
	if len(inputs) < 1:
		print('Error: parse takes at least one argument.', file=sys.stderr)
	elif len(inputs) > 2:
		print('Error: parse takes at most two arguments.', file=sys.stderr)
	elif len(inputs) == 1:
		print('Parsing from one analysis file...')
		handle = from_file(inputs[0])
		json = parse(*handle)
		output = output or default_output(inputs[0])
		print(f'Writing to {output}...')
		write_back(json, output)
	elif len(inputs) == 2:
		print('Parsing from a gmon and program file...')
		handle = gprof(*inputs)
		json = parse(*handle)
		output = output or default_output(inputs[1])
		print(f'Writing to {output}...')
		write_back(json, output)

main_cli.add_command(json)

@click.command()
@click.argument('inputs', nargs=-1, required=True, type=click.Path(exists=True))
def diff(inputs):
	"""Compare multiple json profiles.

	INPUTS can be a single or multiple json files created by coprof json
	"""
	compare(*read(inputs))

main_cli.add_command(diff)
