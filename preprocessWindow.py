import customtkinter as ctk

from Widgets.filterpanel import FilterPanel
from CTkMessagebox import CTkMessagebox

class preprocess(ctk.CTkFrame):
	def __init__(self, master, dataframe):
		super().__init__(master)
		self.grid_columnconfigure(0, weight = 1) #Darle todo el espacio restante a la Tabla
		self.grid_rowconfigure(0, weight = 1) #Darle todo el espacio restante al ScrollableFrame
		self.nonfilterlist = ['LAT_INI', 'LONG_INI', 'LAT_FIN', 'LONG_FIN', 'LAT_INI', 'Hr_INI', 'Hr_FIN',
				   		'LONG_TOT', 'LONG_PAT', 'DIAME_DISCO', 'PESO', 'WA', 'OBSERV',
				   		'Nºind/Tot', 'Nºind/mes', 'Nºind/est', 'CLAV_GRUP', 'CLA_ORDEN', 'CLAVE_FAM', 'CODIGOSPP', 'CLAVE_SP']

		self.data_filter_frame = FilterPanel(self, dataframe, self.nonfilterlist, width = 150, corner_radius = 5)
		self.data_filter_frame.grid(row = 0, column = 0, sticky = 'nwse', padx = 8, pady = 8)
		self.data_filter_frame.grid_rowconfigure(8, weight = 1)
		self.data_filter_frame.grid_columnconfigure(0, weight = 1)
	
		self.filter_button = ctk.CTkButton(self, text = 'Filtrar datos')
		self.filter_button.grid(row = 2, column = 0, sticky = 'sew', padx = 8)
		
		self.preprocess_button = ctk.CTkButton(self, text = 'Preprocesar datos')
		self.preprocess_button.grid(row = 4, column = 0, sticky = 'sew', padx = 8)

	def preprocess_data(self, df):
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

			except ValueError as e:
				CTkMessagebox(title = 'Error', message = f'Error en la columna "{column}":\n\nUno de los valores está vacío o no coincide con el tipo de dato: Número entero.', icon = 'cancel')
				raise
			except Exception as e:
				CTkMessagebox(title = 'Error', message = f'La columna "{column}" no se encuentra dentro del archivo.', icon = 'cancel')
				raise
		
		for column in columns_to_float:
			try:
				df[column] = df[column].astype(float)
			except ValueError as e:
				CTkMessagebox(title = 'Error', message = f'Error en la columna "{column}":\n\nUno de los valores está vacío o no coincide con el tipo de dato: Número con decimales.', icon = 'cancel')
				raise
			except Exception as e:
				CTkMessagebox(title = 'Error', message = f'La columna "{column}" no se encuentra dentro del archivo.', icon = 'cancel')
				raise
		
		for column in columns_to_str:
			try:
				df[column] = df[column].astype(str)
			except ValueError as e:
				CTkMessagebox(title = 'Error', message = f'Error en la columna "{column}":\n\nUno de los valores está vacío o no coincide con el tipo de dato: Texto.', icon = 'cancel')
				raise
			except Exception as e:
				CTkMessagebox(title = 'Error', message = f'La columna "{column}" no se encuentra dentro del archivo.', icon = 'cancel')
				raise