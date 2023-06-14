import customtkinter as ctk

from Widgets.scrollableinfoframeWidget import ScrollableInfoFrame
from Widgets.scrollablecheckboxWidget import ScrollableCheckBoxFrame
from functions import Data, readDataframe
from Widgets.style import Estilo
from Archivos import *

class upload(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		estilo = Estilo()
		#self.grid_rowconfigure(1, weight = 1)
		self.grid_columnconfigure(1, weight = 1)
		self.grid(sticky = 'nswe')

		self.uploadbutton = ctk.CTkButton(self, text = 'Cargar archivo', command = self.button_callbck)
		self.uploadbutton.grid(row = 1, column = 0, sticky = 'sew', padx = 10, pady = 2)
		self.connectbutton = ctk.CTkButton(self, text = 'Conectar a una base de datos', command = self.button_callbck)
		self.connectbutton.grid(row = 2, column = 0, sticky = 'sew', padx = 10, pady = 2)
		self.filterbutton = ctk.CTkButton(self, text = 'Filtrar registros', command = self.filter_button_callbck)
		self.filterbutton.grid(row = 3, column = 0, sticky = 'sew', padx = 10, pady = (2, 8))
		#self.filterbutton = ctk.CTkButton(self, text='Conectar a una base de datos', command=self.button_callbck)
		#self.filterbutton.grid(row = 0, column = 1, sticky= 'e')

		self.infoFrame = ScrollableInfoFrame(self)
		#self.infoFrame.configure(corner_radius = 5, scrollbar_button_hover_color = self._fg_color, scrollbar_button_color = self._fg_color)
		self.infoFrame.grid(row = 0, column = 0, sticky = 'nsew', padx = 8, pady = 8)
		self.grid_rowconfigure(0, weight=1)
	
		self.infoFrameLabel = ctk.CTkLabel(self.infoFrame, text = 'Información', compound = 'left', font = ctk.CTkFont(size = 15, weight = 'bold'))
		self.infoFrameLabel.grid(row = 0, column = 0, sticky = 'new', padx = 20, pady = 20)
		
		self.frameInfo = ctk.CTkLabel(self.infoFrame, text = 'Número de columnas', corner_radius = 5, font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.frameInfo.grid(row=1, column = 0, sticky = 'new',  padx = 2, pady = 2)
		self.frameInfo = ctk.CTkLabel(self.infoFrame, text = 'Número de registros', corner_radius = 5, font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.frameInfo.grid(row=3, column = 0, sticky = 'new',  padx = 2, pady = 2)
		self.frameInfo = ctk.CTkLabel(self.infoFrame, text = 'Registros repetidos', corner_radius = 5, font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.frameInfo.grid(row=5, column = 0, sticky = 'new',  padx = 2, pady = 2)
		self.frameInfo = ctk.CTkLabel(self.infoFrame, text = 'Registros vacios', corner_radius = 5, font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.frameInfo.grid(row=7, column = 0, sticky = 'new',  padx = 2, pady = 2)

	def button_callbck(self):
		readDataframe(self)
	
	def filter_button_callbck(self):
		self.filterWindow = ToplevelWindow(self)

class ToplevelWindow(ctk.CTkToplevel):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.geometry("400x300")
		self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=self, width=200, item_list = Data.dataframe.columns.to_numpy().tolist())
		self.scrollable_checkbox_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")