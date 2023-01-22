# gui.py
from glob import glob
import numpy as np

import customtkinter as ctk
import tkinter as tk

from typing import Protocol
from graphs import BaseGraph

class Config(Protocol):
	"""Protocol for config file"""
	config_file:str
	config:str

	MAIN_LIST_PATH:str
	SUPER6_MAIN_PATH:str
	SUPER6_ALT_PATH:str
	SUPER6_MAIN_PATH_DEBUG:str
	SUPER6_ALT_PATH_DEBUG:str
	BACKUP_DIR:str
	SPLIT_WAVE_DIR:str
	DEBUG:True

class ListBoxData:
	def __init__(self, name, items, listbox_frame, layout_manager, **kwargs):
		self.name = name
		self.items_list = items
		self.items:ctk.StringVar = ctk.StringVar(name=self.name, value=items)
		self.items.trace_add('write', self.items_changed_callback)
		self.selected_index = ctk.IntVar()
		self.listbox = tk.Listbox(listbox_frame, listvariable=self.items, exportselection=False)
		layout_manager(self.listbox, **kwargs)
		self.listbox.bind("<<ListboxSelect>>", self.on_select)

	def on_select(self, event):
		# Update the selected index variable when an item is selected
		self.update_items(["stuff", "things", "other stuff"])
		self.selected_index.set(event.widget.curselection()[0])
	
	def update_items(self, items:list):
		self.items.set(value=items)

	def get_selected_index(self):
		return self.selected_index.get()

	def items_changed_callback(self, *args):
		print("variable changed via something..")
		print(args)

def listbox_callback(event):
	# Handle the callback for all listboxes
	print("from general callback")
	print(event.widget.curselection())

class MainApplication(ctk.CTkFrame):
	def __init__(self, master=None, config:Config=None):
		super().__init__(master)
		self.master.title("WaveCycler")
		self.master = master
		self.config = config

		self.grid()
		self._create_frames()
		self._create_widgets()

	def _create_frames(self):
		self.button_frame = ctk.CTkFrame(self)
		self.button_frame.grid(row=0, column=0)

		self.listbox_frame = ctk.CTkFrame(self)
		self.listbox_frame.grid(row=1, column=0)

		self.graphs_frame = ctk.CTkFrame(self)
		self.graphs_frame.grid(row=2)

		self.big_graph_frame = ctk.CTkFrame(self.graphs_frame)
		self.big_graph_frame.grid(row=0)

		self.small_graph_frame = ctk.CTkFrame(self.graphs_frame)
		self.small_graph_frame.grid(row=1)

	def _create_widgets(self):
		self.quit_button = ctk.CTkButton(self.button_frame, text='Quit', command=self.master.destroy)
		self.quit_button.grid(row=0, column=0)

		self.load_1_button = ctk.CTkButton(self.button_frame, text='Load box 1', command=self.load_listbox1)
		self.load_1_button.grid(row=1, column=0)

		# create three instances of the ListBoxData class, using 'grid' as the layout manager
		self.listbox1 = ListBoxData("List 1", ["Item 1", "Item 2", "Item 3"], self.listbox_frame, tk.Listbox.grid, row=0, column=0)
		self.listbox2 = ListBoxData("List 2", ["Item A", "Item B", "Item C"], self.listbox_frame, tk.Listbox.grid, row=0, column=1)
		self.listbox3 = ListBoxData("List 3", ["Item x", "Item y", "Item z"], self.listbox_frame, tk.Listbox.grid, row=1, column=0)

		# Bind the generic callback function to all listboxes
		self.listbox_frame.bind("<<ListboxSelect>>", listbox_callback)

		self.big_graph = BaseGraph(frame=self.big_graph_frame, nrows=2, ncols=1, figsize=(10,5))
		self.big_graph.grid()
		self.big_graph._test_sine()

		self.small_graphs = BaseGraph(frame=self.small_graph_frame, nrows=2, ncols=16, figsize=(10,5))
		self.small_graphs.grid()
		self.small_graphs._test()

	# create function to update the listbox items
	def update_listbox(self, listbox, items:list):
		listbox.update_items(items)

	def load_listbox1(self):
		self.update_listbox(self.listbox1, ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"])