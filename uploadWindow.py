from datetime import datetime
from tkinter import ttk
import customtkinter as ctk
import pandas as pd
import os

from Widgets.scrollablecheckboxWidget import ScrollableCheckBoxFrame
from tkinter.filedialog import askopenfilename
from CTkMessagebox import CTkMessagebox
from CTkXYFrame import *
from CTkTable import *

from preprocessWindow import preprocess
from capturesWindow import captures
from speciesWindow import species
from mapWindow import maps
from dataframe import Data

class upload(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.grid(sticky= 'nswe')
		self.grid_columnconfigure(1, weight = 1) #Darle todo el espacio restante a la Tabla
		self.grid_rowconfigure(0, weight = 1) #Darle todo el espacio restante al ScrollableFrame

		self.infoFrame = ctk.CTkScrollableFrame(self)
		self.infoFrame.configure(corner_radius = 5)
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
		
		self.frame = ctk.CTkFrame(self)
		self.frame.grid(row = 0, column = 1, rowspan = 4, sticky = 'nswe', padx = 2, pady = 8)
		self.frame.grid_rowconfigure(1, weight = 1)
		self.frame.grid_columnconfigure(0, weight = 1)

		self.searchFrame = ctk.CTkFrame(self.frame, fg_color = 'transparent')
		self.searchFrame.grid(row = 0, column = 0, sticky = 'ew', padx = 10, pady = (8, 0))
		self.searchFrame.grid_rowconfigure(0, weight = 1)

		self.searchButton = ctk.CTkButton(self.searchFrame, text = 'Buscar', state = 'disabled', command = self.searchOnDataframe)
		self.searchButton.grid(row = 0, column = 0, sticky = 'w', padx = (0, 5))

		self.rowTextBox = ctk.CTkEntry(self.searchFrame, width = 180, placeholder_text = 'Ingresa un registro a buscar')
		self.rowTextBox.configure(state = 'disabled')
		self.rowTextBox.grid(row = 0, column = 1, sticky = 'ew')
		
		self.scrollFrame = CTkXYFrame(self.frame, fg_color = 'transparent')
		self.scrollFrame.grid(row = 1, column = 0, sticky = 'nswe', pady = (2, 0))

	def readDataframe(self):
		try:
			file = askopenfilename(initialdir = 'C://', filetypes = [('Excel', '*.xlsx *.xls'), ('CSV', '*.csv'), ('Todos los archivos', '*.*')])
			if file:
				path, extension = os.path.splitext(file)
				match extension:
					case '.csv':
						Data.dataframe = pd.read_csv(file)
					case '.xlsx':
						Data.dataframe = pd.read_excel(file)

				CTkMessagebox(title = 'Aviso', message = 'Archivo cargado con éxito', icon = 'check')
			else:
				CTkMessagebox(title = 'Error', message = 'No se ha seleccionado ningún archivo', icon = 'cancel')
				return
		
		except Exception as e:
			CTkMessagebox(title = 'Error', message = f'Error inesperado: {str(e)}', icon = 'warning')
			return

		self.changeDType(Data.dataframe)
		self.showInfo(Data.dataframe)
		self.createTable(Data.dataframe)

		#self.master.master.preprocessFrame = preprocess(self.master)

		self.master.master.upload_button.configure(command = lambda: self.master.master.select_frame_by_name('upload'))
		self.master.master.preprocess_button.configure(state = 'normal')

	def showInfo(self, df):
		self.DataCol = ctk.CTkLabel(self.infoFrame, text = len(df.columns))
		self.DataRegis = ctk.CTkLabel(self.infoFrame, text = len(df.index))
		self.DataRepeat = ctk.CTkLabel(self.infoFrame, text = df.duplicated().sum())
		self.DataEmpty = ctk.CTkLabel(self.infoFrame, text = df.isnull().sum())
		self.DataCol.grid(row = 2, column = 0, sticky ='ew', pady = (0, 2))
		self.DataRegis.grid(row = 4, column = 0, sticky ='ew', pady = (0, 2))
		self.DataRepeat.grid(row = 6, column = 0, sticky ='ew', pady = (0, 2))
		self.DataEmpty.grid(row = 8, column = 0, sticky ='ew', pady = (0, 2))

		self.filterFrame = ctk.CTkScrollableFrame(self)
		self.filterFrame.configure(corner_radius = 5)
		#self.filterFrame.grid(row = 0, column = 0, sticky = 'nwse', padx = 8, pady = 8)
		self.filterFrame.grid_rowconfigure(8, weight = 1)
		self.filterFrame.grid_columnconfigure(0, weight = 1)
	
		self.filterLabel = ctk.CTkLabel(self.filterFrame, text = 'Filtros', font = ctk.CTkFont(size = 15, weight = 'bold'))
		self.filterLabel.grid(row = 0, column = 0, padx = 20, pady = 20)

		self.Label_Project = ctk.CTkLabel(self.filterFrame, text = 'Proyecto:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Project = ScrollableCheckBoxFrame(self.filterFrame, width=200, item_list = Data.dataframe['PROYECTO/SIP'].unique().tolist(), command = self.updateScrollBox)
		self.Label_Project.grid(row = 1, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Project.grid(row=2, column=0, padx=2, pady=2, sticky='ns')

		self.Label_Year = ctk.CTkLabel(self.filterFrame, text = 'Año:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Year = ScrollableCheckBoxFrame(self.filterFrame, width=200, item_list = Data.dataframe['AÑO'].unique().tolist(), command = self.updateScrollBox)
		self.Label_Year.grid(row = 3, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Year.grid(row=4, column=0, padx=2, pady=2, sticky='ns')

		self.Label_Date = ctk.CTkLabel(self.filterFrame, text = 'Fecha:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Date = ScrollableCheckBoxFrame(self.filterFrame, width=200, item_list = Data.dataframe['FECHA'].unique().tolist(), command = self.updateScrollBox)
		self.Label_Date.grid(row = 5, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Date.grid(row = 6, column = 0, padx = 2, pady = 2, sticky = 'ew')
			
		self.Label_Area = ctk.CTkLabel(self.filterFrame, text = 'Área:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Area = ScrollableCheckBoxFrame(self.filterFrame, width=200, item_list = Data.dataframe['AREA'].unique().tolist(), command = self.updateScrollBox)
		self.Label_Area.grid(row = 7, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Area.grid(row = 8, column = 0, padx = 2, pady = 2, sticky = 'ew')
			
		self.Label_Reg = ctk.CTkLabel(self.filterFrame, text = 'Región:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Reg = ScrollableCheckBoxFrame(self.filterFrame, width=200, item_list = Data.dataframe['REGION'].unique().tolist(), command = self.updateScrollBox)
		self.Label_Reg.grid(row = 9, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Reg.grid(row = 10, column = 0, padx = 2, pady = 2, sticky = 'ew')
			
		self.Label_Reg = ctk.CTkLabel(self.filterFrame, text = 'Subzona:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Sub = ScrollableCheckBoxFrame(self.filterFrame, width=200, item_list = Data.dataframe['SUBZONA'].unique().tolist(), command = self.updateScrollBox)
		self.Label_Reg.grid(row = 11, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Sub.grid(row = 12, column = 0, padx = 2, pady = 2, sticky = 'ew')
		
		self.filterbutton = ctk.CTkButton(self, text = 'Filtrar datos', command = self.Filter_callbck)
		#self.filterbutton.grid(row = 2, column = 0, sticky = 'sew', padx = 8, pady = (2, 8))
		
		self.preprocessbutton = ctk.CTkButton(self, text = 'Preprocesar datos', command = self.preprocessbutton_callbck)
		#self.preprocessbutton.grid(row = 3, column = 0, sticky = 'sew', padx = 8, pady = (2, 8))

	def createTable(self, df):
		try:
			df_list = df.values.tolist()
			column_names = df.columns.tolist()
			df_list.insert(0, column_names)

			#CTkTable Option
			self.table = CTkTable(self.scrollFrame, row = 21, hover_color = '#778899', values = df_list, command = self.UpdateData)
			self.table.grid(row = 0, column = 0)
			self.rowTextBox.configure(state = 'normal')
			self.searchButton.configure(state = 'normal')
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

	def UpdateData(self, data):					
		msn = 'Introduce un nuevo valor\n{}\n\nFila: {}\tColumna: {}'.format(data['value'], data['row'], data['column'])
		dialog = ctk.CTkInputDialog(text = msn, title = 'Modificar valor')

		new_value = dialog.get_input()
		new_index = self.rowTextBox.get()

		if new_index is not None and new_index != '':
			try:
				new_index = int(new_index)
				new_index = new_index - 1
				if new_index >= 0 and new_index <= Data.dataframe.index[-1]:
					data['row'] = new_index
					self.filtertable.insert(1, data['column'], new_value)
					self.table.insert(data['row']+1, data['column'], new_value)
				else:
					CTkMessagebox(title = 'Error', message = 'El valor introducido es mayor a la cantidad de registros', icon = 'cancel')
					return
			except:
				CTkMessagebox(title = 'Error', message = 'El valor introducido no es un número', icon = 'cancel')
				return

		try:
			new_value = new_value.strip()
		except:
			pass

		if new_value is not None and new_value != '':
			self.table.insert(data['row'], data['column'], new_value)

			col_name = self.table.get_column(data['column'])
			col_name = col_name[0]

			if col_name in ['Hr_INI', 'Hr_FIN']:
				new_value = datetime.strptime(new_value, '%H:%M:%S').time()
			else:
				match Data.dataframe[col_name].dtype:
					case 'int64':
						new_value = int(new_value)
					case 'int32':
						new_value = int(new_value)
					case 'float32':
						new_value = float(new_value)
					case 'float64':
						new_value = float(new_value)
					case 'object':
						new_value = str(new_value)
					case 'datetime64[ns]':
						new_value = pd.to_datetime(new_value)
					case _:
						print('Tipo de dato no reconocido: ', Data.dataframe[col_name].dtype)

			if not Data.dataframe[col_name].isin([new_value]).any():
				Data.dataframe.iat[data['row'], data['column']] = new_value
				
				match col_name:
					case 'PROYECTO/SIP':
						self.destroywidgets(self.Scroll_Check_Project, col_name, 2)
					case 'AÑO':
						self.destroywidgets(self.Scroll_Check_Year, col_name, 4)
					case 'FECHA':
						self.destroywidgets(self.Scroll_Check_Date, col_name, 6)
					case 'AREA':
						self.destroywidgets(self.Scroll_Check_Area, col_name, 8)
					case 'REGION':
						self.destroywidgets(self.Scroll_Check_Reg, col_name, 10)
					case 'SUBZONA':
						self.destroywidgets(self.Scroll_Check_Sub, col_name, 12)

	def destroywidgets(self, widget, col_name, irow):
		widget.grid_forget()
		widget.destroy()
		widget = ScrollableCheckBoxFrame(self.filterFrame, width=200, item_list = Data.dataframe[col_name].unique().tolist())
		widget.grid(row = irow, column = 0, padx = 2, pady = 2, sticky = 'ew')
	
	def searchOnDataframe(self):
		new_value = self.rowTextBox.get()
		if new_value is None or new_value == '':
			try:
				self.filtertable.grid_forget()
				self.table.grid()
			except:
				return
		else:
			try:
				index = int(new_value)
				index = index - 1
				if index >= 0 and index <= Data.dataframe.index[-1]:
					df = Data.dataframe.iloc[[index]]
					df_list = df.values.tolist()
					column_names = df.columns.tolist()
					df_list.insert(0, column_names)

					self.table.grid_forget()
					self.filtertable = CTkTable(self.scrollFrame, hover_color = '#778899', values = df_list, command = self.UpdateData)
					self.filtertable.grid(row = 0, column = 0)
				else:
					CTkMessagebox(title = 'Error', message = 'El valor introducido es mayor o menor a la cantidad de registros', icon = 'cancel')
					return
			except:
				CTkMessagebox(title = 'Error', message = 'El valor introducido no es un número', icon = 'cancel')
				return

	def Filter_callbck(self):
		try:
			self.table.destroy()

			project_items = self.Scroll_Check_Project.get_checked_items()
			year_items = self.Scroll_Check_Year.get_checked_items()
			date_items = self.Scroll_Check_Date.get_checked_items()
			area_items = self.Scroll_Check_Area.get_checked_items()
			region_items = self.Scroll_Check_Reg.get_checked_items()
			subzone_items = self.Scroll_Check_Sub.get_checked_items()

			filtered_df = Data.dataframe.copy()

			if project_items:
				filtered_df = filtered_df[filtered_df['PROYECTO/SIP'].isin(project_items)]
			if year_items:
				filtered_df = filtered_df[filtered_df['AÑO'].isin(year_items)]
			if date_items:
				filtered_df = filtered_df[filtered_df['FECHA'].isin(date_items)]
			if area_items:
				filtered_df = filtered_df[filtered_df['AREA'].isin(area_items)]
			if region_items:
				filtered_df = filtered_df[filtered_df['REGION'].isin(region_items)]
			if subzone_items:
				filtered_df = filtered_df[filtered_df['SUBZONA'].isin(subzone_items)]

			df_list = filtered_df.values.tolist()
			column_names = filtered_df.columns.tolist()
			df_list.insert(0, column_names)
			
			self.table = CTkTable(self.scrollFrame, row = 21, hover_color = '#778899', values = df_list, command = self.UpdateData)
			self.table.grid(row = 0, column = 1, rowspan = 2, sticky = 'nsew', padx = 8, pady = 8)
		except:
			pass

	def preprocessbutton_callbck(self):
		self.master.master.mapsFrame = maps(self.master)
		self.master.master.mapsFrame.grid_remove()

		self.master.master.capturesFrame = captures(self.master)
		self.master.master.capturesFrame.grid_remove()

		self.master.master.speciesFrame = species(self.master)
		self.master.master.speciesFrame.grid_remove()

		self.master.master.captures_menu_button.configure(state = 'normal')
		self.master.master.species_menu_button.configure(state = 'normal')
		self.master.master.maps_menu_button.configure(state = 'normal')

	
	def updateScrollBox(self):
		project_items = self.Scroll_Check_Project.get_checked_items()
		year_items = self.Scroll_Check_Year.get_checked_items()
		date_items = self.Scroll_Check_Date.get_checked_items()
		area_items = self.Scroll_Check_Area.get_checked_items()
		region_items = self.Scroll_Check_Reg.get_checked_items()
		subzone_items = self.Scroll_Check_Sub.get_checked_items()

		filtered_df = Data.dataframe.copy()

		if project_items:
			filtered_df = filtered_df[filtered_df['PROYECTO/SIP'].isin(project_items)]
		if year_items:
			filtered_df = filtered_df[filtered_df['AÑO'].isin(year_items)]
		if date_items:
			filtered_df = filtered_df[filtered_df['FECHA'].isin(date_items)]
		if area_items:
			filtered_df = filtered_df[filtered_df['AREA'].isin(area_items)]
		if region_items:
			filtered_df = filtered_df[filtered_df['REGION'].isin(region_items)]
		if subzone_items:
			filtered_df = filtered_df[filtered_df['SUBZONA'].isin(subzone_items)]
		
		self.update_checkboxes_based_on_filter(filtered_df)

	def update_checkboxes_based_on_filter(self, filtered_df):
		# Obtener las listas de elementos únicos para cada columna después de aplicar el filtro
		unique_projects = filtered_df['PROYECTO/SIP'].unique().tolist()
		unique_years = filtered_df['AÑO'].unique().tolist()
		unique_dates = filtered_df['FECHA'].unique().tolist()
		unique_areas = filtered_df['AREA'].unique().tolist()
		unique_regions = filtered_df['REGION'].unique().tolist()
		unique_subzones = filtered_df['SUBZONA'].unique().tolist()

		# Obtener los elementos seleccionados para cada conjunto de checkboxes antes de la actualización
		current_project_items = self.Scroll_Check_Project.get_checked_items()
		current_year_items = self.Scroll_Check_Year.get_checked_items()
		current_date_items = self.Scroll_Check_Date.get_checked_items()
		current_area_items = self.Scroll_Check_Area.get_checked_items()
		current_region_items = self.Scroll_Check_Reg.get_checked_items()
		current_subzone_items = self.Scroll_Check_Sub.get_checked_items()

		# Actualizar los elementos de los checkboxes para mostrar solo los elementos filtrados
		self.Scroll_Check_Project.update_items(unique_projects)
		self.Scroll_Check_Year.update_items(unique_years)
		self.Scroll_Check_Date.update_items(unique_dates)
		self.Scroll_Check_Area.update_items(unique_areas)
		self.Scroll_Check_Reg.update_items(unique_regions)
		self.Scroll_Check_Sub.update_items(unique_subzones)

		# Volver a seleccionar los elementos previamente seleccionados después de la actualización
		for item in current_project_items:
			self.Scroll_Check_Project.set_checked(item)
		for item in current_year_items:
			self.Scroll_Check_Year.set_checked(item)
		for item in current_date_items:
			self.Scroll_Check_Date.set_checked(item)
		for item in current_area_items:
			self.Scroll_Check_Area.set_checked(item)
		for item in current_region_items:
			self.Scroll_Check_Reg.set_checked(item)
		for item in current_subzone_items:
			self.Scroll_Check_Sub.set_checked(item)