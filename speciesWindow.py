import matplotlib.pyplot as plt
import customtkinter as ctk
import seaborn as sns

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from Widgets.scrollablecheckboxWidget import ScrollableCheckBoxFrame
from dataframe import Data

class species(ctk.CTkFrame):
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
		
		self.Label_Species = ctk.CTkLabel(self.infoFrame, text = 'Especie:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Species = ScrollableCheckBoxFrame(self.infoFrame, width=200, item_list = Data.dataframe['ESPECIE'].unique().tolist())
		self.Label_Species.grid(row = 1, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Species.grid(row = 2, column = 0, padx = 2, pady = 2, sticky = 'ew')

		self.Label_Fam = ctk.CTkLabel(self.infoFrame, text = 'Familia:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Fam = ScrollableCheckBoxFrame(self.infoFrame, width=200, item_list = Data.dataframe['FAMILIA'].unique().tolist(), command = self.updateScrollBox)
		self.Label_Fam.grid(row = 3, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Fam.grid(row = 4, column = 0, padx = 2, pady = 2, sticky = 'ew')
			
		self.Label_Group = ctk.CTkLabel(self.infoFrame, text = 'Grupo:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.Scroll_Check_Group = ScrollableCheckBoxFrame(self.infoFrame, width=200, item_list = Data.dataframe['GRUPO'].unique().tolist(), command = self.updateScrollBox)
		self.Label_Group.grid(row = 5, column = 0, sticky = 'w', padx = 4)
		self.Scroll_Check_Group.grid(row = 6, column = 0, padx = 2, pady = 2, sticky = 'ew')

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

		axs[0].pie(df['DIA/NOCHE'].value_counts(), autopct='%1.1f%%', colors=['skyblue', 'lightcoral'])
		axs[0].set_title('Porcentaje de lances de día y de noche', fontsize = 10)
		labels = df['DIA/NOCHE'].unique()
		axs[0].legend(labels, loc = 'upper right')

		etiquetas_personalizadas = {1: 'Hembra', 2: 'Macho', 3: 'Indeterminado'}
		df['SEXO'] = df['SEXO'].map(etiquetas_personalizadas)
		axs[1].pie(df['SEXO'].value_counts(), autopct='%1.1f%%', colors=['skyblue', 'lightcoral', 'blueviolet'])
		axs[1].set_title('Porcentaje de sexos', fontsize = 10)
		labels = df['SEXO'].unique()
		axs[1].legend(labels, loc = 'upper right')
		
		sns.boxplot(x='LONG_TOT', data=df, ax = axs[2])
		axs[2].set_title('Distribución de longitud de especies', fontsize = 10)
		axs[2].set_xlabel('')

		sns.boxplot(x='PESO', data=df, ax = axs[3])
		axs[3].set_title('Distribución de peso de especies', fontsize = 10)
		axs[3].set_xlabel('')

		plt.tight_layout()

		return fig

	def Filter_callbck(self):
		try:
			self.Dashboard_Frame.destroy()
			self.Dashboard_Frame = ctk.CTkScrollableFrame(self)
			self.Dashboard_Frame.grid(row = 0, column = 1, rowspan = 2, sticky = 'nsew', padx = 8, pady = 8)

			specie_items = self.Scroll_Check_Species.get_checked_items()
			fam_items = self.Scroll_Check_Fam.get_checked_items()
			group_items = self.Scroll_Check_Group.get_checked_items()

			filtered_df = Data.dataframe.copy()

			if specie_items:
				filtered_df = filtered_df[filtered_df['ESPECIE'].isin(specie_items)]
			if fam_items:
				filtered_df = filtered_df[filtered_df['FAMILIA'].isin(fam_items)]
			if group_items:
				filtered_df = filtered_df[filtered_df['GRUPO'].isin(group_items)]
		
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
		specie_items = self.Scroll_Check_Species.get_checked_items()
		fam_items = self.Scroll_Check_Fam.get_checked_items()
		group_items = self.Scroll_Check_Group.get_checked_items()

		filtered_df = Data.dataframe.copy()

		if specie_items:
			filtered_df = filtered_df[filtered_df['ESPECIE'].isin(specie_items)]
		if fam_items:
			filtered_df = filtered_df[filtered_df['FAMILIA'].isin(fam_items)]
		if group_items:
			filtered_df = filtered_df[filtered_df['GRUPO'].isin(group_items)]
		
		self.update_checkboxes_based_on_filter(filtered_df)

	def update_checkboxes_based_on_filter(self, filtered_df):
		# Obtener las listas de elementos únicos para cada columna después de aplicar el filtro
		unique_species = filtered_df['ESPECIE'].unique().tolist()
		unique_fams = filtered_df['FAMILIA'].unique().tolist()
		unique_groups = filtered_df['GRUPO'].unique().tolist()

		# Obtener los elementos seleccionados para cada conjunto de checkboxes antes de la actualización
		current_specie_items = self.Scroll_Check_Species.get_checked_items()
		current_fam_items = self.Scroll_Check_Fam.get_checked_items()
		current_group_items = self.Scroll_Check_Group.get_checked_items()

		# Actualizar los elementos de los checkboxes para mostrar solo los elementos filtrados
		self.Scroll_Check_Species.update_items(unique_species)
		self.Scroll_Check_Fam.update_items(unique_fams)
		self.Scroll_Check_Group.update_items(unique_groups)

		# Volver a seleccionar los elementos previamente seleccionados después de la actualización
		for item in current_specie_items:
			self.Scroll_Check_Species.set_checked(item)
		for item in current_fam_items:
			self.Scroll_Check_Fam.set_checked(item)
		for item in current_group_items:
			self.Scroll_Check_Group.set_checked(item)