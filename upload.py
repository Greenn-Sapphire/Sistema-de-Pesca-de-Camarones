import customtkinter as ctk
import pandas as pd
from Recursos.style import Estilo
from tkinter.filedialog import askopenfilename
from CTkMessagebox import CTkMessagebox
from CTkTable import *
from Archivos import *
import configparser

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

		self.infoFrame = ctk.CTkFrame(self, corner_radius = 5)
		self.infoFrame.grid(row = 0, column = 0, rowspan = 2, sticky= 'nwse', padx=8, pady=8)
		self.infoFrame.grid_columnconfigure(0, weight=1)
		self.infoFrame.grid_rowconfigure(8, weight=1)
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
		try:
			filename = askopenfilename(initialdir="C://")
			dataframe = pd.read_csv(filename, sep=',|;', engine="python", on_bad_lines='skip')
			settings = configparser.ConfigParser()
			settings.read('config.ini')
			settings['SETTINGS']['dataframe_path'] = filename
			with open('config.ini', 'w') as configfile:
				settings.write(configfile)

			if 'table' in locals():
				self.frame.destroy()
				self.frameInfo.destroy()

			self.frame = ctk.CTkScrollableFrame(self, orientation='horizontal', fg_color='transparent')
			self.frame.grid(row = 1, column = 1, sticky = 'nswe', padx=10, pady=5)
			table = CTkTable(self.frame, row = 20, column_names=[dataframe.columns.to_numpy().tolist()] ,values=dataframe.to_numpy().tolist())
			table.grid(row= dataframe.shape[0], column= dataframe.shape[1])

			self.frameInfo = ctk.CTkLabel(self.infoFrame, text = len(dataframe.columns))
			self.frameInfo.grid(row=2, column = 0, sticky='n')

			self.frameInfo = ctk.CTkLabel(self.infoFrame, text = len(dataframe.index))
			self.frameInfo.grid(row=4, column = 0, sticky='n')
	
			self.frameInfo = ctk.CTkLabel(self.infoFrame, text = dataframe.duplicated().sum())
			self.frameInfo.grid(row=6, column = 0, sticky='n')

			self.frameInfo = ctk.CTkLabel(self.infoFrame, text = dataframe.isnull().sum())
			self.frameInfo.grid(row=8, column = 0, sticky='n')
		except:
			CTkMessagebox(title="Error", message="El archivo es inválido", icon="cancel")