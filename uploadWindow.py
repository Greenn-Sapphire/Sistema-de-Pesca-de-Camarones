import customtkinter as ctk
import os
import pandas as pd

from tkinter.filedialog import askopenfilename
from CTkMessagebox import CTkMessagebox
from CTkTable import *
from CTkXYFrame import *
from Widgets.scrollablecheckboxWidget import ScrollableCheckBoxFrame
from Widgets.style import Estilo
from dataframe import Data
from preprocessWindow import preprocess

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
		
		self.uploadbutton = ctk.CTkButton(self, text = 'Cargar archivo', command = self.readDataframe)
		self.uploadbutton.grid(row = 1, column = 0, sticky = 'sew', padx = 8, pady = (2, 8))
		
		self.frame = CTkXYFrame(self)
		self.frame.grid(row = 0, column = 1, rowspan = 4, sticky = 'nswe', padx = 2, pady = 8)

	def readDataframe(self):
		try:
			file = askopenfilename(initialdir = 'C://', filetypes = [('Excel', '*.xlsx'), ('CSV', '*.csv')])
			path, extension = os.path.splitext(file)
			match extension:
				case '.csv':
					Data.dataframe = pd.read_csv(file, sep = ',|;', engine = 'python', on_bad_lines = 'skip')
				case '.xlsx':
					Data.dataframe = pd.read_excel(file)

			self.changeDType(Data.dataframe)
			self.showInfo(Data.dataframe)
			self.createTable(Data.dataframe)

			self.master.master.preprocessFrame = preprocess(self.master)
			self.master.master.preprocessFrame.grid_forget()
			self.master.master.uploadFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 10, pady = 10)

			self.master.master.upload_button.configure(command = self.master.master.upload_button_event)
			self.master.master.preprocess_button.configure(state = 'normal')

			CTkMessagebox(title = 'Aviso', message = 'Tabla creada con éxito', icon = 'check')
		except:
			CTkMessagebox(title = 'Error', message = 'No se ha seleccionado ningún archivo', icon = 'cancel')
			return

	def showInfo(self, df):
		self.DataCol = ctk.CTkLabel(self.infoFrame, text = len(df.columns))
		self.DataRegis = ctk.CTkLabel(self.infoFrame, text = len(df.index))
		self.DataRepeat = ctk.CTkLabel(self.infoFrame, text = df.duplicated().sum())
		self.DataEmpty = ctk.CTkLabel(self.infoFrame, text = df.isnull().sum())
		self.DataCol.grid(row = 2, column = 0, sticky ='ew', pady = (0, 2))
		self.DataRegis.grid(row = 4, column = 0, sticky ='ew', pady = (0, 2))
		self.DataRepeat.grid(row = 6, column = 0, sticky ='ew', pady = (0, 2))
		self.DataEmpty.grid(row = 8, column = 0, sticky ='ew', pady = (0, 2))

	def createTable(self, df):
		try:
			df_list = df.values.tolist()
			column_names = df.columns.tolist()
			df_list.insert(0, column_names)
			
			self.table = CTkTable(self.frame, row = 30, hover_color = '#778899', values = df_list)
			self.table.grid(row = 0, column = 0)
		except:
			CTkMessagebox(title = 'Error', message = 'La tabla no se pudo crear', icon = 'cancel')
			return

	def changeDType(self, df):
		df['PROYECTO/SIP'] = df['PROYECTO/SIP'].astype(int)
		df['AÑO'] = df['AÑO'].astype(int)
		df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y').dt.strftime('%d/%m/%Y')  # Convertir a tipo datetime
		df['BARCO'] = df['BARCO'].astype(str)
		df['CRUCERO'] = df['CRUCERO'].astype(int)
		df['AREA'] = df['AREA'].astype(str)
		df['REGION'] = df['REGION'].astype(str)
		df['SUBZONA'] = df['SUBZONA'].astype(int)
		df['ESTACION'] = df['ESTACION'].astype(int)
		df['LANCE'] = df['LANCE'].astype(int)

		df['LAT_INI'] = df['LAT_INI'].astype(int)
		df['LONG_INI'] = df['LONG_INI'].astype(int)
		df['LAT_FIN'] = df['LAT_FIN'].astype(int)
		df['LONG_FIN'] = df['LONG_FIN'].astype(int)
		df['LAT_INI'] = df['LAT_INI'].astype(int)

		df['Hr_INI'] = pd.to_datetime(df['Hr_INI'], format='%H:%M:%S').dt.time  # Convertir a tipo time
		df['Hr_FIN'] = pd.to_datetime(df['Hr_FIN'], format='%H:%M:%S').dt.time  # Convertir a tipo time
		df['DURACION'] = df['DURACION'].astype(int)  # Convertir a tipo timedelta
		df['DIA/NOCHE'] = df['DIA/NOCHE'].astype(str)
		df['PROF/m'] = df['PROF/m'].astype(float)
		df['PLATAF'] = df['PLATAF'].astype(str)
		df['ESTRATO PROF.'] = df['ESTRATO PROF.'].astype(str)

		df['T °C'] = df['T °C'].astype(int)
		df['SALIN (0/00)'] = df['SALIN (0/00)'].astype(int)
		df['FAC/kg'] = df['FAC/kg'].astype(float)
		df['Camaron/kg'] = df['Camaron/kg'].astype(float)

		df['GRUPO'] = df['GRUPO'].astype(str)
		df['CLAV_GRUP'] = df['CLAV_GRUP'].astype(str)
		df['ORDEN'] = df['ORDEN'].astype(str)
		df['CLA_ORDEN'] = df['CLA_ORDEN'].astype(str)
		df['FAMILIA'] = df['FAMILIA'].astype(str)
		df['CLAVE_FAM'] = df['CLAVE_FAM'].astype(str)
		df['CLAVE_SP'] = df['CLAVE_SP'].astype(str)
		df['CODIGOSPP'] = df['CODIGOSPP'].astype(str)
		df['ESPECIE'] = df['ESPECIE'].astype(str)

		df['Nºind/Tot'] = df['Nºind/Tot'].fillna(0)
		df['Nºind/Tot'] = df['Nºind/Tot'].astype(int)
		df['Nºind/mes'] = df['Nºind/mes'].astype(int)
		df['Nºind/est'] = df['Nºind/est'].astype(int)
		df['LONG_TOT'] = df['LONG_TOT'].astype(float)
		df['LONG_PAT'] = df['LONG_PAT'].astype(float)
		df['DIAME_DISCO'] = df['DIAME_DISCO'].astype(float)
		df['PESO'] = df['PESO'].astype(float)
		df['SEXO'] = df['SEXO'].fillna(3)
		df['SEXO'] = df['SEXO'].astype(int)
		df['EDO_MAD'] = df['EDO_MAD'].fillna(0)
		df['EDO_MAD'] = df['EDO_MAD'].astype(int)
		df['WA'] = df['WA'].astype(float)
		df['OBSERV'] = df['OBSERV'].astype(str)

class ToplevelWindow(ctk.CTkToplevel):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.geometry("400x300")
		self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=self, width=200, item_list = Data.dataframe['ESPECIE'].unique().tolist())
		self.scrollable_checkbox_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")