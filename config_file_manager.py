# config_file_manager.py
import os
import toml
import tomllib
from dataclasses import dataclass, field

@dataclass
class TomlConfigFile():
	"""Default config.toml is generated if not found."""
	config_file:str = field(init=False, default="config.toml")
	config = dict()

	def __post_init__(self):
		if not os.path.exists(self.config_file):
			self._generate_default_file()
		with open(self.config_file, "rb") as f:
			self.config = tomllib.load(f)
		self.MAIN_LIST_PATH = self.config["paths"]["main_list"]
		self.SUPER6_MAIN_PATH = self.config["paths"]["super6_main_list"]
		self.SUPER6_ALT_PATH = self.config["paths"]["super6_alt_list"]
		self.SUPER6_MAIN_PATH_DEBUG = self.config["debugpaths"]["super6_main_list"]
		self.SUPER6_ALT_PATH_DEBUG = self.config["debugpaths"]["super6_alt_list"]
		self.BACKUP_DIR = self.config["paths"]["backup_directory"]
		self.SPLIT_WAVE_DIR = self.config["paths"]["wavesplit_directory"]
		self.DEBUG = self.config["runmode"]["debug"] == "1"

	def _generate_default_file(self):
		config = {
			"title": "Configuration",
			"runmode": {
				"debug":"1"
			},
			"paths": {
			"main_list": "./wavs",
			"backup_directory": "./wavs/wave_backup",
			"wavesplit_directory": "./wavs/wave_splits",
			"super6_main_list": "/VOLUMES/SUPER6/waveforms",
			"super6_alt_list": "/VOLUMES/SUPER6/alt_waveforms",
			"output_main_list": "/VOLUMES/SUPER6/waveforms",
			"output_alt_list": "/VOLUMES/SUPER6/alt_waveforms"
			},
			"debugpaths": {
				"super6_main_list": "./wavs/debug_folder/waveforms",
				"super6_alt_list": "./wavs/debug_folder/alt_waveforms",
				"output_main_list": "./wavs/debug_folder/waveforms",
				"output_alt_list": "./wavs/debug_folder/alt_waveforms"
			}
		}
		with open(self.config_file, "w") as f:
			toml.dump(config, f)