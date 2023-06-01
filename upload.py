import customtkinter as ctk
from Recursos.style import Estilo
from Archivos import *
from functions import readDataframe
from Recursos.widgets import Options_Widget

class upload(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		estilo = Estilo()
		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(1, weight=1)
		self.grid(sticky= 'nswe')

		self.uploadbutton = ctk.CTkButton(self, text="Cargar archivo", command=self.button_callbck)
		self.uploadbutton.grid(row = 0, column = 1, sticky= 'w', pady=8)
		self.connectbutton = ctk.CTkButton(self, text="Conectar a una base de datos", command=self.button_callbck)
		self.connectbutton.grid(row = 0, column = 1, sticky= 'e', pady=8)
		#self.filterbutton = ctk.CTkButton(self, text="Conectar a una base de datos", command=self.button_callbck)
		#self.filterbutton.grid(row = 0, column = 1, sticky= 'e')

		self.infoFrame = Options_Widget(self, 0, 0, 0, 8)
		self.infoFrameLabel = ctk.CTkLabel(self.infoFrame, text="Información", compound="left", font=ctk.CTkFont(size=15, weight="bold"))
		self.infoFrameLabel.grid(row=0, column=0, padx=20, pady=20)
		
		self.frameInfo = ctk.CTkLabel(self.infoFrame, text = 'Número de columnas', corner_radius=5, font=ctk.CTkFont(size=12, weight="bold"))
		self.frameInfo.grid(row=1, column = 0, sticky='n',  padx=5, pady=2)
		self.frameInfo = ctk.CTkLabel(self.infoFrame, text = 'Número de registros', corner_radius=5, font=ctk.CTkFont(size=12, weight="bold"))
		self.frameInfo.grid(row=3, column = 0, sticky='n',  padx=5, pady=2)
		self.frameInfo = ctk.CTkLabel(self.infoFrame, text = 'Registros repetidos', corner_radius=5, font=ctk.CTkFont(size=12, weight="bold"))
		self.frameInfo.grid(row=5, column = 0, sticky='n',  padx=5, pady=2)
		self.frameInfo = ctk.CTkLabel(self.infoFrame, text = 'Registros vacios', corner_radius=5, font=ctk.CTkFont(size=12, weight="bold"))
		self.frameInfo.grid(row=7, column = 0, sticky='n',  padx=5, pady=2)

	def button_callbck(self):
		readDataframe(self)