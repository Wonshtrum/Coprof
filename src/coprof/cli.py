"""
Command line of coprof
"""

import click
import coprof

@click.group()
def main_cli():
	"""−−−−−−−−−−−−−−−−−  COPROF  −−−−−−−−−−−−−−−−−

You are now using te command line interface of Coprof
a Python3 helper to compare profiling data, created at CERFACS (https://cerfacs.fr).

This is a python package currently installed in your python environment.
"""
	pass


@click.command()
@click.argument("a")
def test(a):
	print(a)

main_cli.add_command(test)
