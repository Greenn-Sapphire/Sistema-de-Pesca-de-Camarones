import customtkinter as ctk
import seaborn as sns
import pandas as pd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from Widgets.scrollablecheckboxWidget import ScrollableCheckBoxFrame
import matplotlib.pyplot as plt
from dataframe import Data

class captures(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.grid_remove()
		self.grid(sticky= 'nswe')
		self.grid_columnconfigure(1, weight = 1)
		self.grid_rowconfigure(0, weight = 1)

		self.infoFrame = ctk.CTkScrollableFrame(self)
		self.infoFrame.configure(corner_radius = 5)
		self.infoFrame.grid(row = 0, column = 0, sticky = 'nwse', padx = 8, pady = 8)
		self.infoFrame.grid_rowconfigure(6, weight = 1)
		self.infoFrame.grid_columnconfigure(0, weight = 1)
		
		self.infoLabel = ctk.CTkLabel(self.infoFrame, text = 'Filtros', font = ctk.CTkFont(size = 15, weight = 'bold'))
		self.infoLabel.grid(row = 0, column = 0, padx = 20, pady = 20)
		
		self.Label_Project = ctk.CTkLabel(self.infoFrame, text = 'Proyecto:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Project = ScrollableCheckBoxFrame(self.infoFrame, width=200, item_list = Data.dataframe['PROYECTO/SIP'].unique().tolist(), command = self.updateScrollBox)
		self.Label_Project.grid(row = 1, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Project.grid(row=2, column=0, padx=2, pady=2, sticky='ns')

		self.Label_Year = ctk.CTkLabel(self.infoFrame, text = 'Año:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Year = ScrollableCheckBoxFrame(self.infoFrame, width=200, item_list = Data.dataframe['AÑO'].unique().tolist(), command = self.updateScrollBox)
		self.Label_Year.grid(row = 3, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Year.grid(row=4, column=0, padx=2, pady=2, sticky='ns')

		self.Label_Date = ctk.CTkLabel(self.infoFrame, text = 'Fecha:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Date = ScrollableCheckBoxFrame(self.infoFrame, width=200, item_list = Data.dataframe['FECHA'].unique().tolist(), command = self.updateScrollBox)
		self.Label_Date.grid(row = 5, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Date.grid(row = 6, column = 0, padx = 2, pady = 2, sticky = 'ew')
			
		self.Label_Area = ctk.CTkLabel(self.infoFrame, text = 'Área:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Area = ScrollableCheckBoxFrame(self.infoFrame, width=200, item_list = Data.dataframe['AREA'].unique().tolist(), command = self.updateScrollBox)
		self.Label_Area.grid(row = 7, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Area.grid(row = 8, column = 0, padx = 2, pady = 2, sticky = 'ew')
			
		self.Label_Reg = ctk.CTkLabel(self.infoFrame, text = 'Región:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Reg = ScrollableCheckBoxFrame(self.infoFrame, width=200, item_list = Data.dataframe['REGION'].unique().tolist(), command = self.updateScrollBox)
		self.Label_Reg.grid(row = 9, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Reg.grid(row = 10, column = 0, padx = 2, pady = 2, sticky = 'ew')
			
		self.Label_Sub = ctk.CTkLabel(self.infoFrame, text = 'Subzona:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Sub = ScrollableCheckBoxFrame(self.infoFrame, width=200, item_list = Data.dataframe['SUBZONA'].unique().tolist(), command = self.updateScrollBox)
		self.Label_Sub.grid(row = 11, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Sub.grid(row = 12, column = 0, padx = 2, pady = 2, sticky = 'ew')

		self.Button = ctk.CTkButton(self, text = 'Aplicar filtros', command = self.Filter_callbck)
		self.Button.grid(row = 1, column = 0, sticky = 'ew', padx = 8, pady = (2, 8))

		self.Dashboard_Frame = ctk.CTkScrollableFrame(self)
		self.Dashboard_Frame.grid(row = 0, column = 1, rowspan = 2, sticky = 'nsew', padx = 8, pady = 8)

		fig = self.createPlots(Data.dataframe)

		# Crear el lienzo de la gráfica y agregarlo al marco
		self.canvas = FigureCanvasTkAgg(fig, master = self.Dashboard_Frame)
		self.canvas.draw()
		self.canvas.get_tk_widget().configure(bg = 'lightgray', highlightthickness = 0)
		self.canvas.get_tk_widget().pack()

		toolbar = NavigationToolbar2Tk(self.canvas, self.Dashboard_Frame)
		toolbar.update()
		toolbar.pack()

	def createPlots(self, df):
		# Crear los datos y generar la gráfica usando Seaborn
		fig, axs = plt.subplots(4, figsize=(9, 16), facecolor='none')

		conteo_especies = df['ESPECIE'].value_counts()
		conteo_especies_top20 = conteo_especies.head(20)
		axs[0].grid(True, linestyle = '--', alpha = 0.5)
		sns.barplot(x=conteo_especies_top20.values, y=conteo_especies_top20.index, ax = axs[0])

		# Agregar etiquetas y título
		axs[0].set_title('Conteo de las primeras 10 especies más capturadas', fontsize = 10)
		axs[0].tick_params(axis = 'x', labelsize = 8)
		axs[0].tick_params(axis = 'y', labelsize = 8)


		conteo_grupos = df['GRUPO'].value_counts()
		axs[1].grid(True, linestyle = '--', alpha = 0.5)
		sns.barplot(x=conteo_grupos.values, y=conteo_grupos.index, ax = axs[1])

		# Agregar etiquetas y título
		axs[1].set_title('Cantidad de Especies por Grupo', fontsize = 10)
		axs[1].tick_params(axis = 'x', labelsize = 8)
		axs[1].tick_params(axis = 'y', labelsize = 8)

		
		data_grouped = df.groupby('PROF/m').agg({'Camaron/kg': 'sum', 'FAC/kg': 'sum'}).reset_index()
		axs[2].grid(True, linestyle = '--', alpha = 0.5)
		sns.barplot(x='PROF/m', y='FAC/kg', data=data_grouped, color='orange', label='FAC/kg', ax = axs[2])
		sns.barplot(x='PROF/m', y='Camaron/kg', data=data_grouped, color='blue', label='Camaron/kg', ax = axs[2])

		#Agregar leyendas y etiquetas
		axs[2].set_xlabel('')
		axs[2].set_ylabel('')
		axs[2].set_title('KG de Camarón y FAC capturado por Prof.', fontsize = 10)
		axs[2].tick_params(axis = 'x', labelsize = 8)
		axs[2].tick_params(axis = 'y', labelsize = 8)
		lines, labels = axs[2].get_legend_handles_labels()
		axs[2].legend(lines, labels)


		# Crear la gráfica de lineas
		df_resampled = df.copy()
		df_resampled['FECHA'] = pd.to_datetime(df_resampled['FECHA'], format='%d/%m/%Y')
		df_resampled.set_index('FECHA', inplace=True)
		df_resampled = df_resampled.resample('D')['ESPECIE'].count()
		axs[3].grid(True, linestyle = '--', alpha = 0.5)
		sns.lineplot(x=df_resampled.index, y=df_resampled.values, data=df_resampled, ax = axs[3])

		# Agregar etiquetas y título
		axs[3].set_xlabel('')
		axs[3].set_ylabel('')
		axs[3].set_title('Total de especies capturadas por día', fontsize = 10)
		axs[3].tick_params(axis = 'x', labelsize = 8)
		axs[3].tick_params(axis = 'y', labelsize = 8)
		axs[3].set_xticks(axs[3].get_xticks())

		plt.tight_layout()

		return fig

	def Filter_callbck(self):
		try:
			self.Dashboard_Frame.destroy()
			self.Dashboard_Frame = ctk.CTkScrollableFrame(self)
			self.Dashboard_Frame.grid(row = 0, column = 1, rowspan = 2, sticky = 'nsew', padx = 8, pady = 8)

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
		
			fig = self.createPlots(filtered_df)

			self.canvas = FigureCanvasTkAgg(fig, master = self.Dashboard_Frame)
			self.canvas.draw()
			self.canvas.get_tk_widget().configure(bg = 'lightgray', highlightthickness = 0)
			self.canvas.get_tk_widget().pack()

			toolbar = NavigationToolbar2Tk(self.canvas, self.Dashboard_Frame)
			toolbar.update()
			toolbar.pack()
		except:
			pass
	
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