from sys import argv, stderr, exit
import json
import re
from .config import categories


def help():
	print(f'Use: {argv[0]} analysis.txt [output]', file=stderr)
	print(f'or: {argv[0]} -a gmon.out program [output]', file=stderr)


class Holder:
	categories = categories
	def __init__(self):
		self.data = {}
	def add_entry(self):
		raise RuntimeError
	def dump(self):
		return json.dumps(self.data, indent=4)

class Short(Holder):
	def add_entry(self, entry):
		name = entry[-1]
		profile = [float(value) if value else None for value in entry[:-1]]
		self.data[name] = profile

class Medium(Holder):
	def add_entry(self, entry):
		name = entry[-1]
		profile = {category:float(value) for category, value in zip(Medium.categories, entry) if value}
		self.data[name] = profile

class Long(Holder):
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
	end_header_re = re.compile(r'^ time\s+seconds\s+seconds\s+calls\s+s/call\s+s/call\s+name\s*$')
	data_section = False
	result = holder()

	with handle as flux:
		# Read until end of gprof flat profile header
		while not data_section:
			line = readline(flux)
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
		line = readline(flux)
		while line and len(line) > 1:
			start_column = columns[0]
			entry = []
			for end_column in columns[1:]:
				entry.append(line[start_column:end_column].replace(' ', ''))
				start_column = end_column
			result.add_entry(entry)
			line = readline(flux)
	return result.dump()


def gprof(gmon, program):
	import subprocess as sp
	handle = sp.Popen(['gprof', program, gmon], stdout=sp.PIPE)
	access = lambda flux: flux.stdout.readline().decode()
	return handle, access

def from_file(path):
	handle = open(argv[1], 'r')
	access = lambda flux: flux.readline()
	return handle, access

def default_output(path):
	if path[-4:] in ('.txt', '.out'):
		path = path[:-4]
	return path+'.json'

def write_back(output, path):
	with open(path, 'w') as fout:
		fout.write(output)


if __name__ == '__main__':
	length = len(argv)
	assemble = length > 1 and argv[1] == '-a'
	full_length = 5 if assemble else 3
	if length == full_length:
		output = argv[-1]
	elif length == full_length-1:
		output = default_output(argv[-1])
	else:
		help()
		exit()

	if assemble:
		handle = gprof(argv[2], argv[3])
	else:
		handle = from_file(argv[1])
	write_back(parse(*handle), output)
