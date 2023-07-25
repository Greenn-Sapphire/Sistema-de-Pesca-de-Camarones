import customtkinter as ctk
import pandas as pd
from CTkTable import *
from CTkXYFrame import *
from Widgets.scrollablecheckboxWidget import ScrollableCheckBoxFrame

from datetime import datetime
from Widgets.style import Estilo
from dataframe import Data
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

		self.Label_Project = ctk.CTkLabel(self.infoFrame, text = 'Proyecto:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Project = ScrollableCheckBoxFrame(self.infoFrame, width=200, item_list = Data.dataframe['PROYECTO/SIP'].unique().tolist())
		self.Label_Project.grid(row = 1, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Project.grid(row=2, column=0, padx=2, pady=2, sticky="ns")

		self.Label_Year = ctk.CTkLabel(self.infoFrame, text = 'Año:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Year = ScrollableCheckBoxFrame(self.infoFrame, width=200, item_list = Data.dataframe['AÑO'].unique().tolist())
		self.Label_Year.grid(row = 3, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Year.grid(row=4, column=0, padx=2, pady=2, sticky="ns")

		self.Label_Date = ctk.CTkLabel(self.infoFrame, text = 'Fecha:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Date = ScrollableCheckBoxFrame(self.infoFrame, width=200, item_list = Data.dataframe['FECHA'].unique().tolist())
		self.Label_Date.grid(row = 5, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Date.grid(row = 6, column = 0, padx = 2, pady = 2, sticky = 'ew')
			
		self.Label_Area = ctk.CTkLabel(self.infoFrame, text = 'Área:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Area = ScrollableCheckBoxFrame(self.infoFrame, width=200, item_list = Data.dataframe['AREA'].unique().tolist())
		self.Label_Area.grid(row = 7, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Area.grid(row = 8, column = 0, padx = 2, pady = 2, sticky = 'ew')
			
		self.Label_Reg = ctk.CTkLabel(self.infoFrame, text = 'Región:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Reg = ScrollableCheckBoxFrame(self.infoFrame, width=200, item_list = Data.dataframe['REGION'].unique().tolist())
		self.Label_Reg.grid(row = 9, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Reg.grid(row = 10, column = 0, padx = 2, pady = 2, sticky = 'ew')
			
		self.Label_Reg = ctk.CTkLabel(self.infoFrame, text = 'Subzona:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Sub = ScrollableCheckBoxFrame(self.infoFrame, width=200, item_list = Data.dataframe['SUBZONA'].unique().tolist())
		self.Label_Reg.grid(row = 11, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Sub.grid(row = 12, column = 0, padx = 2, pady = 2, sticky = 'ew')
		
		self.uploadbutton = ctk.CTkButton(self, text = 'Preprocesar datos', command = self.button_callbck)
		self.uploadbutton.grid(row = 1, column = 0, sticky = 'sew', padx = 8, pady = (2, 8))

		self.frame = CTkXYFrame(self)
		self.frame.grid(row = 0, column = 1, rowspan = 4, sticky = 'nswe', padx = 2, pady = 8)
		
		try:
			df_list = Data.dataframe.values.tolist()
			column_names = Data.dataframe.columns.tolist()
			df_list.insert(0, column_names)
		except Exception as e:
			print(e)
		
		self.table = CTkTable(self.frame, row = 30, hover_color = '#778899', values = df_list, command = self.UpdateData)
		self.table.grid(row = 0, column = 0)

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

	def UpdateData(self, data):
		msn = "Introduce un nuevo valor\n{}\n\nFila: {}\tColumna: {}".format(data['value'], data['row'], data['column'])
		dialog = ctk.CTkInputDialog(text = msn, title = "Modificar valor")

		new_value = dialog.get_input()
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
						print("Tipo de dato no reconocido: ", Data.dataframe[col_name].dtype)

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
		widget = ScrollableCheckBoxFrame(self.infoFrame, width=200, item_list = Data.dataframe[col_name].unique().tolist())
		widget.grid(row = irow, column = 0, padx = 2, pady = 2, sticky = 'ew')