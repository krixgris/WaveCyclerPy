# file_handler.py

from dataclasses import dataclass, field
import os


@dataclass(slots=True)
class File:
	"""index: manually index to maintain lookupability"""
	index:int = field(repr=True)
	filename:str = field(repr=False)
	name:str = field(init=False, repr=True)
	simple_name:str = field(init=False, repr=False)
	extension:str = field(init=False, repr=False)
	rel_path:str = field(init=False, repr=False)

	def __post_init__(self):
		self.name:str = os.path.basename(self.filename)
		self.simple_name:str = os.path.splitext(self.name)[0]
		self.extension = os.path.splitext(self.filename)[1]
		self.rel_path:str = os.path.relpath(self.filename)

	def __lt__(self, other):
         return self.name < other.name
	
def friendly_file_list(file_list:list[File]):
	return [f.name for f in file_list]