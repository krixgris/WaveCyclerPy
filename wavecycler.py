# wavecycler.py

import customtkinter as ctk

from config_file_manager import TomlConfigFile
import gui

def main() -> None:
	root = ctk.CTk()
	cfg = TomlConfigFile()
	app = gui.MainApplication(root, cfg)
	app.mainloop()

if __name__ == '__main__':
	main()