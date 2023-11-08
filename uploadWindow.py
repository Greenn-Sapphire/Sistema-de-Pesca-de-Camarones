import customtkinter as ctk
import pandas as pd
import os

from Widgets.informationpanel import InformationPanel
from tkinter.filedialog import askopenfilename
from Widgets.tableWidget import TableWidget
from CTkMessagebox import CTkMessagebox

class upload(ctk.CTkFrame):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		self.grid_columnconfigure(0, weight = 1) #Darle todo el espacio restante a la Tabla
		self.grid_rowconfigure(0, weight = 1) #Darle todo el espacio restante al ScrollableFrame

		self.data_information_frame = InformationPanel(self, width = 150, corner_radius = 5)
		self.data_information_frame.grid(row = 0, column = 0, sticky = 'nwse', padx = 8, pady = 8)
		self.data_information_frame.grid_rowconfigure(10, weight = 1)
		self.data_information_frame.grid_columnconfigure(0, weight = 1)
		
		self.upload_button = ctk.CTkButton(self, text = 'Cargar archivo')
		self.upload_button.grid(row = 1, column = 0, sticky = 'sew', padx = 8, pady = (2, 8))

	def readData(self):
		dataframe = pd.DataFrame({})
		try:
			file = askopenfilename(initialdir = 'C://', filetypes = [('Excel', '*.xlsx *.xls'), ('CSV', '*.csv')])
			if file:
				path, extension = os.path.splitext(file)
				match extension:
					case '.csv':
						dataframe = pd.read_csv(file)
					case '.xlsx':
						dataframe = pd.read_excel(file)

				def remove_accents(input_str):
					accents = {
						'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
						'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'
					}
					return ''.join(accents.get(char, char) for char in input_str)

				# Aplicar la función a los nombres de las columnas
				dataframe.columns = [remove_accents(col) for col in dataframe.columns]

				dataframe['FECHA'] = pd.to_datetime(dataframe['FECHA'], format='%d/%m/%Y').dt.strftime('%d/%m/%Y')  # Convertir a tipo datetime
				dataframe['Hr_INI'] = pd.to_datetime(dataframe['Hr_INI'], format='%H:%M:%S').dt.time  # Convertir a tipo time
				dataframe['Hr_FIN'] = pd.to_datetime(dataframe['Hr_FIN'], format='%H:%M:%S').dt.time  # Convertir a tipo time

				CTkMessagebox(title = 'Aviso', message = 'Archivo cargado con éxito', icon = 'check')
				return dataframe
			
			else:
				CTkMessagebox(title = 'Error', message = 'No se ha seleccionado ningún archivo', icon = 'cancel')
				return dataframe
		
		except Exception as e:
			CTkMessagebox(title = 'Error', message = f'Error inesperado: {str(e)}', icon = 'warning')
			return dataframe

	def createTable(self, master, dataframe):
		try:
			df_list = dataframe.values.tolist()
			column_names = dataframe.columns.tolist()
			df_list.insert(0, column_names)

			table_frame = TableWidget(master, df_list, dataframe, corner_radius = 5)
			table_frame.grid_rowconfigure(1, weight = 1)
			table_frame.grid_columnconfigure(0, weight = 1)
			return table_frame
		
		except Exception as e:
			print(e)
			CTkMessagebox(title = 'Error', message = 'La tabla no se pudo crear', icon = 'cancel')