from sys import argv, stderr, exit
import json
from .config import categories

import tkinter
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

def help():
	print(f'Use {argv[0]} analysis.json [analysis2.json,...]', file=stderr)


def read(files):
	programs = []
	names = []
	for name in files:
		try:
			with open(name, 'r') as fin:
				programs.append(json.loads(fin.read()))
				names.append(name.replace('.json', ''))
		except Exception as e:
			print(f'Couldn\'t load {name} due to:\n{e}', file=stderr)
	return programs, names


def get_functions(programs):
	functions = set()
	for program in programs:
		functions.update(program.keys())
	return list(functions)

def collect(programs, functions):
	aggregate = []
	for function in functions:
		costs = []
		for program in programs:
			costs.append(program.get(function))
		aggregate.append((function, costs))
	return aggregate

def select(aggregate, key):
	selection = [(name, [cost.get(key) if cost else None for cost in costs]) for name, costs in aggregate]
	selection.sort(key=lambda costs:sum(cost for cost in costs[1] if cost is not None), reverse=True)
	return selection


def static_compare(programs, names):
	for program in programs:
		#print(program.keys())
		pass


class Graph:
	VERTICAL = 0
	HORIZONTAL = 1
	def __init__(self, programs, names, key=categories[0], limit=10, direction=HORIZONTAL, reverse=False):
		self.key = key
		self.direction = direction
		self.reverse = reverse
		self.programs = programs
		self.names = names
		self.functions = get_functions(programs)
		self.aggregate = collect(programs, self.functions)
		self.selection = select(self.aggregate, key)
		self.limit = min(limit, len(self.functions))

		self.fig, self.ax = plt.subplots()

		root  = tkinter.Tk()

		frame = tkinter.Frame(root)
		frame.pack()

		self.list_categories = ttk.Combobox(frame, values=categories)
		self.list_categories.current(0)
		self.list_categories.bind("<<ComboboxSelected>>", self.update_category)
		self.list_categories.pack(side=tkinter.LEFT)

		self.spin_limit = tkinter.Spinbox(frame, from_=1, to=len(self.functions), command=self.update_limit)
		self.spin_limit.pack(side=tkinter.LEFT)

		self.check_direction = ttk.Checkbutton(frame, text="Vertical", command=self.update_direction)
		self.check_direction.pack(side=tkinter.LEFT)

		self.canvas = FigureCanvasTkAgg(self.fig, master=root)
		self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
		#toolbar = NavigationToolbar2Tk(self.canvas, root)
		#toolbar.update()
		self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

		self.draw()

		tkinter.mainloop()
	
	def update_category(self, event):
		self.key = self.list_categories.get()
		self.selection = select(self.aggregate, self.key)
		self.draw()
	def update_direction(self):
		checked = self.check_direction.instate(['selected'])
		self.direction = Graph.VERTICAL if checked else Graph.HORIZONTAL
		self.draw()
	def update_limit(self):
		self.limit = int(self.spin_limit.get())
		self.draw()

	def draw(self):
		plt.cla()

		selection = self.selection[:self.limit]
		functions = [function for function, _ in selection]
		series = list(zip(*[costs for _, costs in selection]))
		size = len(functions)

		if self.direction == Graph.VERTICAL:
			bar = self.ax.bar
			set_fun_label = self.ax.set_xlabel
			set_cst_label = self.ax.set_ylabel
			set_ticks = self.ax.set_xticks
			set_ticklabels = self.ax.set_xticklabels
			text = lambda x, y: plt.text(x, y, y, ha='center', va='bottom')
		else:
			bar = self.ax.barh
			set_fun_label = self.ax.set_ylabel
			set_cst_label = self.ax.set_xlabel
			set_ticks = self.ax.set_yticks
			set_ticklabels = self.ax.set_yticklabels
			text = lambda x, y: plt.text(y, x, y, ha='left', va='center')

		bar_width = 0.3
		bar_space = 1.1
		fun_space = 0.3
		n_labels = [sum(bar_width*bar_space for cost in costs if cost is not None)+fun_space for _, costs in selection]
		p_labels = [0]*size
		for i in range(1, size):
			p_labels[i] = p_labels[i-1]+n_labels[i-1]

		#set_fun_label('Functions')
		set_cst_label(self.key)
		#self.ax.set_title('Test')
		set_ticks([p+(w-fun_space-bar_width)/2 for p, w in zip(p_labels, n_labels)])
		set_ticklabels(functions)

		for i, name in enumerate(self.names):
			bars_width = [0 if _ is None else bar_width for _ in series[i]]
			bar(p_labels, [0 if _ is None else _ for _ in series[i]], bars_width, label=name)
			for j, cost in enumerate(series[i]):
				if cost is not None:
					text(p_labels[j], cost)
			p_labels = [p+w*bar_space for p, w in zip(p_labels, bars_width)]
		
		self.ax.legend()
		self.canvas.draw()


def compare(programs, names):
	if not programs:
		print('Not a single file has been successfully decoded', file=stderr)
		return
	if len(programs) > 1:
		static_compare(programs, names)
	Graph(programs, names)

if __name__ == '__main__':
	if len(argv) < 2:
		help()
	else:
		compare(*read(argv[1:]))
