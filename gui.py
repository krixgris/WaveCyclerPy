# gui.py
import customtkinter as ctk
import tkinter as tk

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
	print(event.widget.curselection())



class MainApplication(ctk.CTkFrame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.grid()
		self.create_widgets()

	def create_widgets(self):
		self.quit_button = ctk.CTkButton(self, text='Quit', command=self.master.destroy)
		self.quit_button.grid()

		self.load_1_button = ctk.CTkButton(self, text='Load box 1', command=self.load_listbox1)
		self.load_1_button.grid()
				
		# Create a frame to hold the listboxes
		self.listbox_frame = ctk.CTkFrame(self)
		self.listbox_frame.grid()
		# create three instances of the ListBoxData class, using 'grid' as the layout manager
		self.listbox1 = ListBoxData("List 1", ["Item 1", "Item 2", "Item 3"], self.listbox_frame, tk.Listbox.grid, row=0, column=0)
		self.listbox2 = ListBoxData("List 2", ["Item A", "Item B", "Item C"], self.listbox_frame, tk.Listbox.grid, row=0, column=1)
		self.listbox3 = ListBoxData("List 3", ["Item x", "Item y", "Item z"], self.listbox_frame, tk.Listbox.grid, row=1, column=0)

		# Bind the generic callback function to all listboxes
		self.listbox_frame.bind("<<ListboxSelect>>", listbox_callback)

	# create function to update the listbox items
	def update_listbox(self, listbox, items:list):
		listbox.update_items(items)

	def load_listbox1(self):
		self.update_listbox(self.listbox1, ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"])