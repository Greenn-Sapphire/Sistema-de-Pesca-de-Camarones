import customtkinter as ctk

from Widgets.scrollablecheckboxWidget import ScrollableCheckBoxFrame
from functions import readDataframe, select_frame_by_name
from Widgets.style import Estilo
from dataframe import Data

class upload(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		estilo = Estilo()
		self.grid(sticky= 'nswe')
		self.grid_columnconfigure(1, weight = 1) #Darle todo el espacio restante a la Tabla
		self.grid_rowconfigure(0, weight = 1) #Darle todo el espacio restante al ScrollableFrame

		self.infoFrame = ctk.CTkScrollableFrame(self)
		self.infoFrame.configure(corner_radius = 5, scrollbar_button_hover_color = ('gray86', 'gray17'), scrollbar_button_color = ('gray81', 'gray20'))
		self.infoFrame.grid(row = 0, column = 0, sticky = 'nwse', padx = 8, pady = 8)
		self.infoFrame.grid_rowconfigure(8, weight = 1)
		self.infoFrame.grid_columnconfigure(0, weight = 1)
	
		self.infoLabel = ctk.CTkLabel(self.infoFrame, text = 'Información', font = ctk.CTkFont(size = 15, weight = 'bold'))
		self.infoLabel.grid(row = 0, column = 0, padx = 20, pady = 20)
		
		self.Label_ColNum = ctk.CTkLabel(self.infoFrame, text = 'Número de columnas', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Label_Regis = ctk.CTkLabel(self.infoFrame, text = 'Número de registros', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Label_Repeat = ctk.CTkLabel(self.infoFrame, text = 'Registros repetidos', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Label_Empty = ctk.CTkLabel(self.infoFrame, text = 'Registros vacios', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Label_ColNum.grid(row = 1, column = 0, sticky = 'ew', pady = (2, 0))
		self.Label_Regis.grid(row = 3, column = 0, sticky = 'ew', pady = (2, 0))
		self.Label_Repeat.grid(row = 5, column = 0, sticky = 'ew', pady = (2, 0))
		self.Label_Empty.grid(row = 7, column = 0, sticky = 'ew', pady = (2, 0))
		
		self.uploadbutton = ctk.CTkButton(self, text = 'Cargar archivo', command = self.button_callbck)
		self.uploadbutton.grid(row = 1, column = 0, sticky = 'sew', padx = 8, pady = (2, 8))

	def button_callbck(self):
		readDataframe(self, self.master)
		self.master.master.upload_button.configure(command=self.master.master.upload_button_event)
		self.master.master.preprocess_button.configure(state = 'normal')

	
	def filter_button_callbck(self):
		self.filterWindow = ToplevelWindow(self)

class ToplevelWindow(ctk.CTkToplevel):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.geometry("400x300")
		self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=self, width=200, item_list = Data.dataframe['ESPECIE'].unique().tolist())
		self.scrollable_checkbox_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")