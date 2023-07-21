import customtkinter as ctk

from Widgets.style import Estilo
from dataframe import Data
from Widgets.tableWidget import Table
from mapWindow import maps
from capturesWindow import captures
from speciesWindow import species

class preprocess(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		estilo = Estilo()
		self.grid(sticky= 'nswe')
		self.grid_columnconfigure(1, weight = 1) #Darle todo el espacio restante a la Tabla
		self.grid_rowconfigure(0, weight = 1) #Darle todo el espacio restante al ScrollableFrame

		self.infoFrame = ctk.CTkScrollableFrame(self)
		self.infoFrame.configure(corner_radius = 5)
		self.infoFrame.grid(row = 0, column = 0, sticky = 'nwse', padx = 8, pady = 8)
		self.infoFrame.grid_rowconfigure(8, weight = 1)
		self.infoFrame.grid_columnconfigure(0, weight = 1)
	
		self.infoLabel = ctk.CTkLabel(self.infoFrame, text = 'Filtros', font = ctk.CTkFont(size = 15, weight = 'bold'))
		self.infoLabel.grid(row = 0, column = 0, padx = 20, pady = 20)

		Table(self, Data.dataframe, 'preprocess')
		
		self.uploadbutton = ctk.CTkButton(self, text = 'Preprocesar datos', command = self.button_callbck)
		self.uploadbutton.grid(row = 1, column = 0, sticky = 'sew', padx = 8, pady = (2, 8))

	def button_callbck(self):
		self.master.master.mapsFrame = maps(self.master)
		self.master.master.mapsFrame.grid_forget()

		self.master.master.capturesFrame = captures(self.master)
		self.master.master.capturesFrame.grid_forget()

		self.master.master.speciesFrame = species(self.master)
		self.master.master.speciesFrame.grid_forget()

		self.master.master.captures_menu_button.configure(state = 'normal')
		self.master.master.species_menu_button.configure(state = 'normal')
		self.master.master.maps_menu_button.configure(state = 'normal')