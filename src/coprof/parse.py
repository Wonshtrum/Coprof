"""
Parse gprof output (from analysis or gmon directly) and create a json containing the flat analysis.
"""
from sys import stderr, exit
import json
import re
from .config import categories


class Holder:
	"""Json holder abstract class.
	An holder is used to construct a json from the flat analysis of gprof.
	The holder is responsible for the json structure.
	The json is stored in the member "data"."""
	categories = categories
	def __init__(self):
		"""Initialise the holder"""
		self.data = {}
	def add_entry(self, entry):
		"""Each line of the flat analysis is to be added with this function.
		The implementation of add_entry determine the final output by the way it interacts with "data"."""
		raise NotImplementedError
	def dump(self):
		"""The holder output the final json by directly converting its member "data"."""
		return json.dumps(self.data, indent=4)

class Short(Holder):
	"""Json holder with short (deprecated) syntax."""
	def add_entry(self, entry):
		name = entry[-1]
		profile = [float(value) if value else None for value in entry[:-1]]
		self.data[name] = profile

class Medium(Holder):
	"""Json holder with medium (default) syntax."""
	def add_entry(self, entry):
		name = entry[-1]
		profile = {category:float(value) for category, value in zip(Medium.categories, entry) if value}
		self.data[name] = profile

class Long(Holder):
	"""Json holder with long (deprecated) syntax."""
	def __init__(self):
		super().__init__()
		self.data['functions'] = []
		self.data['profile'] = {}
	
	def add_entry(self, entry):
		name = entry[-1]
		profile = {category:float(value) for category, value in zip(Long.categories, entry) if value}
		self.data['functions'].append(name)
		self.data['profile'][name] = profile


def parse(handle, readline, holder = Medium):
	"""Given a data stream, a readline function and a data holder, output the corresponding json."""
	end_header_re = re.compile(r'^ time\s+seconds\s+seconds\s+calls\s+s/call\s+s/call\s+name\s*$')
	data_section = False
	result = holder()

	with handle as stream:
		# Read until end of gprof flat profile header
		while not data_section:
			line = readline(stream)
			if not line:
				print('Unexpected EOF, bad format: header wasn\'t found', file=stderr)
				exit()
			data_section = end_header_re.match(line)

		# Get width of each column
		columns = []
		old_char = ' '
		for i, char in enumerate(line):
			if old_char == ' ' and char != ' ':
				columns.append(i)
			old_char = char
		columns[-1] = -1

		# Parse each line of the table
		line = readline(stream)
		while line and len(line) > 1:
			start_column = columns[0]
			entry = []
			for end_column in columns[1:]:
				entry.append(line[start_column:end_column].replace(' ', ''))
				start_column = end_column
			result.add_entry(entry)
			line = readline(stream)
	return result.dump()


def gprof(gmon, program):
	"""Coprof can handle raw gmon file. To do so, the gmon and program files content must be processed by this function.
	The standard gprof analysis is outputed through a data stream and an access method."""
	import subprocess as sp
	try:
		handle = sp.Popen(['gprof', program, gmon], stdout=sp.PIPE)
	except Exception as e:
		print(f'Error: {e}', file=stderr)
		exit()
	access = lambda stream: stream.stdout.readline().decode()
	return handle, access

def from_file(path):
	"""Create a data stream and an access method from a gprof analysis file."""
	handle = open(path, 'r')
	access = lambda stream: stream.readline()
	return handle, access

def default_output(path):
	"""Create a default output file name based on the input file name."""
	if path[-4:] in ('.txt', '.out'):
		path = path[:-4]
	return path+'.json'

def write_back(output, path):
	"""Write the resulting json in an output file for further comparison."""
	with open(path, 'w') as fout:
		fout.write(output)
