# gui.py
from glob import glob
from dataclasses import dataclass, field
import numpy as np
from random import randint
from os import path

import customtkinter as ctk
import tkinter as tk

from typing import Protocol
from graphs import BaseGraph

from file_handler import File, friendly_file_list

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
	"""Has BaseGraph and a tk.Listbox.
	.grid() is exposed from listbox for gui management."""
	def __init__(self, listbox_frame, name, file_path, width=42, height=16, **kwargs):
		self.name = name
		self.file_list = [File(i,f) for i,f in enumerate(glob(f"{file_path}/*.*")) if path.splitext(f)[1] in [".wav",".ws6"]]
		print(self.file_list)
		self.items_list = friendly_file_list(self.file_list)
		self.graph_object:BaseGraph = None
		self.graph_ax_index = None
		self.items:ctk.StringVar = ctk.StringVar(name=self.name, value=friendly_file_list(self.file_list))
		self.items.trace_add('write', self.items_changed_callback)
		self.selected_index = ctk.IntVar()
		self.listbox = tk.Listbox(listbox_frame, listvariable=self.items, exportselection=False, height=height, width=width, **kwargs)
		self.listbox.bind("<<ListboxSelect>>", self.on_select)
		self.grid = self.listbox.grid

	def on_select(self, event):
		self.selected_index.set(event.widget.curselection()[0])
		print(self.file_list[self.selected_index.get()].filename)
		match self.graph_object:
			case BaseGraph():
				self.graph_object.update_ax(self.graph_ax_index, np.random.rand(10+randint(0, 10)))
			case other:
				print("no graph object set")
		
	def set_graph_object(self, graph_object:BaseGraph, ax_index:int=0):
		"""Set the graph object to update when a listbox item is selected
		ax_index is the index of the axis to update on the graph object"""
		self.graph_object = graph_object
		self.graph_ax_index = ax_index
	
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
		print(self.config.MAIN_LIST_PATH)

		self.grid()
		self._create_frames()
		self._create_widgets()

	def _create_frames(self):
		self.button_frame = ctk.CTkFrame(self)
		self.listbox_frame = ctk.CTkFrame(self, height=16)
		self.graphs_frame = ctk.CTkFrame(self)

		self.button_frame.grid(row=0, column=0)
		self.listbox_frame.grid(row=1, column=0, padx=5, pady=5)
		self.graphs_frame.grid(row=2)

		self.big_graph_frame = ctk.CTkFrame(self.graphs_frame)
		self.small_graph_frame = ctk.CTkFrame(self.graphs_frame)
		self.big_graph_frame.grid(row=0)
		self.small_graph_frame.grid(row=1)

	def _create_widgets(self):
		self.quit_button = ctk.CTkButton(self.button_frame, text='Quit', command=self.master.destroy)
		self.load_1_button = ctk.CTkButton(self.button_frame, text='Load box 1', command=self.load_listbox1)

		self.quit_button.grid(row=0, column=0)
		self.load_1_button.grid(row=1, column=0)

		self.listbox1 = ListBoxData(self.listbox_frame, "List 1", self.config.MAIN_LIST_PATH)
		self.listbox2 = ListBoxData(self.listbox_frame, "List 2", self.config.SUPER6_MAIN_PATH_DEBUG)
		self.listbox3 = ListBoxData(self.listbox_frame, "List 3", self.config.SUPER6_ALT_PATH_DEBUG)
		self.listbox4 = ListBoxData(self.listbox_frame, "List 4", self.config.SUPER6_MAIN_PATH_DEBUG)
		self.listbox5 = ListBoxData(self.listbox_frame, "List 5", self.config.SUPER6_ALT_PATH_DEBUG)

		self.listbox1.grid(row=0, column=0)
		self.listbox2.grid(row=0, column=1)
		self.listbox3.grid(row=0, column=2)
		self.listbox4.grid(row=0, column=4)
		self.listbox5.grid(row=0, column=5)

		# Bind the generic callback function to all listboxes
		self.listbox_frame.bind("<<ListboxSelect>>", listbox_callback)

		self.big_graph = BaseGraph(frame=self.big_graph_frame, nrows=2, ncols=1, figsize=(19,5))
		self.big_graph.grid()
		# self.big_graph._test_sine()
		self.main_bank_graph = BaseGraph(frame=self.small_graph_frame, nrows=1, ncols=16, figsize=(19,5))
		self.main_bank_graph.grid()
		self.alt_bank_graph = BaseGraph(frame=self.small_graph_frame, nrows=1, ncols=16, figsize=(19,5))
		self.alt_bank_graph.grid()
		# self.small_graphs._test()

		self.listbox1.set_graph_object(self.big_graph, ax_index=1)
		self.listbox2.set_graph_object(self.main_bank_graph, ax_index=15)
		self.listbox3.set_graph_object(self.alt_bank_graph, ax_index=2)

	def update_listbox(self, listbox, items:list):
		listbox.update_items(items)

	def load_listbox1(self):
		self.update_listbox(self.listbox1, ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"])