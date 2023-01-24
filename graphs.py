# graphs.py
"""Graphs classes for wavecycler.
Contains definitions for graph setup."""
from dataclasses import dataclass, field
from typing import Protocol

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TKFrame(Protocol):
	"""Protocol for TKinter frames"""
	pass


class BaseGraph:
	"""Base class for graphs
	Creates a figure and axes for the graph, as well as a canvas.
	grid and draw are exposed from canvas and tk_widget so they can be used"""
	def __init__(self, frame=TKFrame, nrows=1, ncols=1, figsize=(10,5), **kwargs):
		self.fig, self._ax = plt.subplots(nrows=nrows,ncols=ncols, figsize=figsize)
		self.ax = np.ravel(self._ax)
		self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0.2, wspace=0.2)
		self.fig.set_facecolor("gray")

		self.rows = nrows
		self.cols = ncols
		# self.ax_count = len(self.ax)

		self._canvas_setup(frame=frame)

	
	def _canvas_setup(self, frame=TKFrame):
		"""Inits the canvas and grid"""
		self._test_sine()
		self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
		self.canvas.draw()

		self.grid =	self.canvas.get_tk_widget().grid
		self.draw = self.canvas.draw

	# fill all ax objects with sines
	def _test_sine(self):
		for ax in self.ax:
			ax.clear()
			ax.plot(np.sin(np.linspace(0, 2*np.pi, 100)))
			self.format_ax(ax)

	def _test(self):
		for ax in self.ax:
			ax.clear()
			ax.plot(np.random.rand(10))
			self.format_ax(ax)

	@property
	def length(self):
		"""Returns the number of axes"""
		return len(self.ax)

	def format_ax(self, ax, *args, **kwargs):
		"""Format the axes"""
		ax.axis("off")
		ax.set_title(label=None, fontdict={'fontsize': 8})
		ax.get_lines()[0].set_color("blue")
		ax.get_lines()[0].set_linewidth(2)

	def update_ax(self, ax_num, value:np.ndarray):
		"""Update the axes"""
		print(ax_num)
		if(ax_num >= self.length):
			raise IndexError(f"Unable to update graph, index out of range ({ax_num=})")
		# clear the axes
		self.ax[ax_num].clear()
		self.ax[ax_num].plot(value)
		self.format_ax(self.ax[ax_num])
		# update the graph
		self.canvas.draw()

	def update(self, *args, **kwargs):
		"""Update the graph"""
		pass

	def clear(self):
		"""Clear the graph"""
		pass