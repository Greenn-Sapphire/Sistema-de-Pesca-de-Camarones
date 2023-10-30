import customtkinter as ctk
import pandas as pd
import os

from Widgets.informationpanel import InformationPanel
from tkinter.filedialog import askopenfilename
from Widgets.tableWidget import TableWidget
from Widgets.filterpanel import FilterPanel
from CTkMessagebox import CTkMessagebox
from CTkXYFrame import *
from CTkTable import *

from dashboards import dashboards
from capturesWindow import captures
from speciesWindow import species
from mapWindow import maps
from PIL import Image

class upload(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.grid(sticky= 'nswe')
		self.grid_columnconfigure(1, weight = 1) #Darle todo el espacio restante a la Tabla
		self.grid_rowconfigure(0, weight = 1) #Darle todo el espacio restante al ScrollableFrame

		self.infoWidget = InformationPanel(self, width = 150)
		self.infoWidget.configure(corner_radius = 5)
		self.infoWidget.grid(row = 0, column = 0, sticky = 'nwse', padx = 8, pady = 8)
		self.infoWidget.grid_rowconfigure(10, weight = 1)
		self.infoWidget.grid_columnconfigure(0, weight = 1)
		
		self.uploadbutton = ctk.CTkButton(self, text = 'Cargar archivo', command = self.readData)
		self.uploadbutton.grid(row = 1, column = 0, sticky = 'sew', padx = 8, pady = (2, 8))

	def readData(self):
		try:
			file = askopenfilename(initialdir = 'C://', filetypes = [('Excel', '*.xlsx *.xls'), ('CSV', '*.csv'), ('Todos los archivos', '*.*')])
			if file:
				path, extension = os.path.splitext(file)
				match extension:
					case '.csv':
						self.dataframe = pd.read_csv(file)
					case '.xlsx':
						self.dataframe = pd.read_excel(file)

				def remove_accents(input_str):
					accents = {
						'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
						'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'
					}
					return ''.join(accents.get(char, char) for char in input_str)

				# Aplicar la función a los nombres de las columnas
				self.dataframe.columns = [remove_accents(col) for col in self.dataframe.columns]

				self.dataframe['FECHA'] = pd.to_datetime(self.dataframe['FECHA'], format='%d/%m/%Y').dt.strftime('%d/%m/%Y')  # Convertir a tipo datetime
				self.dataframe['Hr_INI'] = pd.to_datetime(self.dataframe['Hr_INI'], format='%H:%M:%S').dt.time  # Convertir a tipo time
				self.dataframe['Hr_FIN'] = pd.to_datetime(self.dataframe['Hr_FIN'], format='%H:%M:%S').dt.time  # Convertir a tipo time

				CTkMessagebox(title = 'Aviso', message = 'Archivo cargado con éxito', icon = 'check')
			else:
				CTkMessagebox(title = 'Error', message = 'No se ha seleccionado ningún archivo', icon = 'cancel')
				return
		
		except Exception as e:
			CTkMessagebox(title = 'Error', message = f'Error inesperado: {str(e)}', icon = 'warning')
			return

		self.showInfo()
		self.createTable()

		#self.master.master.preprocessFrame = preprocess(self.master)
		self.master.master.upload_button.configure(command = lambda: self.master.master.select_frame_by_name('upload'))
		self.master.master.preprocess_button.configure(state = 'normal')

	def showInfo(self):
		self.infoWidget.showinfo(self.dataframe)
		nonfilterlist = ['LAT_INI', 'LONG_INI', 'LAT_FIN', 'LONG_FIN', 'LAT_INI', 'Hr_INI', 'Hr_FIN', 'Nºind/Tot',
				   'Nºind/mes', 'Nºind/est', 'LONG_TOT', 'LONG_PAT', 'DIAME_DISCO', 'PESO', 'WA',
				   'CLAV_GRUP', 'CLA_ORDEN', 'CLAVE_FAM', 'CODIGOSPP', 'CLAVE_SP', 'OBSERV']

		self.filterFrame = FilterPanel(self, self.dataframe, nonfilterlist, width = 150)
		self.filterFrame.configure(corner_radius = 5)
		#self.filterFrame.grid(row = 0, column = 0, sticky = 'nwse', padx = 8, pady = 8)
		self.filterFrame.grid_rowconfigure(8, weight = 1)
		self.filterFrame.grid_columnconfigure(0, weight = 1)
	
		self.filterbutton = ctk.CTkButton(self, text = 'Filtrar datos', command = self.Filter_callbck)
		#self.filterbutton.grid(row = 2, column = 0, sticky = 'sew', padx = 8, pady = (2, 8))
		
		self.preprocessbutton = ctk.CTkButton(self, text = 'Preprocesar datos', command = self.preprocessbutton_callbck)
		#self.preprocessbutton.grid(row = 3, column = 0, sticky = 'sew', padx = 8, pady = (2, 8))

	def createTable(self):
		try:
			df_list = self.dataframe.values.tolist()
			column_names = self.dataframe.columns.tolist()
			df_list.insert(0, column_names)

			#CTkTable Option
			image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Archivos')
			self.menu_image = ctk.CTkImage(Image.open(os.path.join(image_path, 'settings.png')), size=(20, 20))
			self.frame = TableWidget(self, df_list, self.menu_image, self.dataframe)
			self.frame.grid(row = 0, column = 1, rowspan = 4, sticky = 'nswe', padx = 2, pady = 8)
			self.frame.grid_rowconfigure(1, weight = 1)
			self.frame.grid_columnconfigure(0, weight = 1)
		except:
			CTkMessagebox(title = 'Error', message = 'La tabla no se pudo crear', icon = 'cancel')
			return

	def changeDType(self, df):
		columns_to_int = [
			'PROYECTO/SIP', 'AÑO', 'CRUCERO', 'SUBZONA', 'ESTACION', 'LANCE',
			'LAT_INI', 'LONG_INI', 'LAT_FIN', 'LONG_FIN', 'LAT_INI',
			'T °C', 'SALIN (0/00)', 'Nºind/Tot', 'Nºind/mes', 'Nºind/est',
			'SEXO', 'EDO_MAD']
		columns_to_float = [
			'PROF/m', 'FAC/kg', 'Camaron/kg', 'LONG_TOT', 'LONG_PAT',
			'DIAME_DISCO', 'PESO', 'WA']
		columns_to_str = [
			'BARCO', 'AREA', 'REGION', 'DIA/NOCHE', 'PLATAF', 'ESTRATO PROF.',
			'GRUPO', 'CLAV_GRUP', 'ORDEN', 'CLA_ORDEN', 'FAMILIA', 'CLAVE_FAM',
			'CLAVE_SP', 'CODIGOSPP', 'ESPECIE', 'OBSERV']
		
		for column in columns_to_int:
			try:
				if column == 'Nºind/Tot' or column == 'Nºind/mes' or column == 'Nºind/est' or column == 'EDO_MAD' or column == 'T °C' or column == 'SALIN (0/00)':
					df[column] = df[column].fillna(0)
				
				if column == 'SEXO':
					df[column] = df[column].fillna(3)
				df[column] = df[column].astype(int)

			except Exception as e:
				CTkMessagebox(title = 'Error', message = f'Error en la columna "{column}":\n\n{e}', icon = 'cancel')
				return
		
		for column in columns_to_float:
			try:
				df[column] = df[column].astype(float)
			except Exception as e:
				CTkMessagebox(title = 'Error', message = f'Error en la columna "{column}":\n\n{e}', icon = 'cancel')
				return
		
		for column in columns_to_str:
			try:
				df[column] = df[column].astype(str)
			except Exception as e:
				CTkMessagebox(title = 'Error', message = f'Error en la columna "{column}":\n\n{e}', icon = 'cancel')
				return

		self.master.master.dashboardFrame = dashboards(self.master, self.dataframe)
		self.master.master.dashboardFrame.grid_remove()

		#self.master.master.capturesFrame = captures(self.master, self.dataframe)
		#self.master.master.capturesFrame.grid_remove()

		#self.master.master.speciesFrame = species(self.master, self.dataframe)
		#self.master.master.speciesFrame.grid_remove()

		self.master.master.mapsFrame = maps(self.master, self.dataframe)
		self.master.master.mapsFrame.grid_remove()

		self.master.master.dashboard_menu_button.configure(state = 'normal')
		self.master.master.maps_menu_button.configure(state = 'normal')

	def Filter_callbck(self):
		try:
			self.frame.table.destroy()
			df_list = self.filterFrame.apply_filter()
			
			self.frame.table = CTkTable(self.frame.scrollFrame, row = self.frame.numrow + 1, hover_color = '#778899', values = df_list, command = self.frame.UpdateData)
			self.frame.table.grid(row = 0, column = 0, rowspan = 2, sticky = 'nsew', padx = 8, pady = 8)
		except Exception as e:
			CTkMessagebox(title = 'Error', message = f'Error inesperado: {str(e)}', icon = 'warning')
			return

	def preprocessbutton_callbck(self):
		self.changeDType(self.dataframe)