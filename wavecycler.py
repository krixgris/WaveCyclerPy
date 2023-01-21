# wavecycler.py

import customtkinter as ctk

from config_file_manager import TomlConfigFile
import gui

cfg = TomlConfigFile()

def main() -> None:
	root = ctk.CTk()
	app = gui.MainApplication(root)
	app.mainloop()

if __name__ == '__main__':
	main()