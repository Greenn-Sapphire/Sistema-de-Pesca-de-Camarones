import matplotlib.pyplot as plt
import customtkinter as ctk
import seaborn as sns
import pandas as pd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from CTkMessagebox import CTkMessagebox

class dashboards(ctk.CTkFrame):
	def __init__(self, master, dataframe):
		super().__init__(master)
		self.grid_columnconfigure(1, weight = 1)
		self.grid_rowconfigure(0, weight = 1)
		self.dataframe = dataframe
		
		self.tabs = ctk.CTkTabview(self)
		self.tabs.add('Lances')
		self.tabs.add('Especies')
		self.tabs.set('Lances')
		self.tabs.grid(row = 0, column = 1, rowspan = 2, sticky = 'nsew', padx = 8, pady = 8)

		self.dashboard_captures_frame = ctk.CTkScrollableFrame(self.tabs.tab('Lances'), fg_color='transparent')
		self.dashboard_captures_frame.pack(fill='both', expand=True)

		self.dashboard_species_frame = ctk.CTkScrollableFrame(self.tabs.tab('Especies'), fg_color='transparent')
		self.dashboard_species_frame.pack(fill='both', expand=True)

		self.fig_captures = self.createPlots(self.dataframe)
		
		self.canvas_captures = FigureCanvasTkAgg(self.fig_captures, master = self.dashboard_captures_frame)
		self.canvas_captures.draw()
		self.canvas_captures.get_tk_widget().configure(highlightthickness = 0)
		self.canvas_captures.get_tk_widget().pack(fill='both', expand=True)
		
		toolbar = NavigationToolbar2Tk(self.canvas_captures, self.dashboard_captures_frame)
		toolbar.update()
		toolbar.pack()
		
		self.fig_species = self.createPlots2(self.dataframe)
		
		self.canvas_species = FigureCanvasTkAgg(self.fig_species, master = self.dashboard_species_frame)
		self.canvas_species.draw()
		self.canvas_species.get_tk_widget().configure(highlightthickness = 0)
		self.canvas_species.get_tk_widget().pack(fill='both', expand=True)
		
		toolbar2 = NavigationToolbar2Tk(self.canvas_species, self.dashboard_species_frame)
		toolbar2.update()
		toolbar2.pack()

	def createPlots(self, df):
		# Crear los datos y generar la gráfica usando Seaborn
		fig, axs = plt.subplots(4, figsize=(9, 16), facecolor='none')

		conteo_especies = df['ESPECIE'].value_counts()
		conteo_especies_top20 = conteo_especies.head(20)
		axs[0].grid(True, linestyle = '--', alpha = 0.5)
		sns.barplot(x=conteo_especies_top20.values, y=conteo_especies_top20.index, ax = axs[0], color = 'royalblue')

		# Agregar etiquetas y título
		axs[0].set_title('Conteo de las primeras 20 especies más capturadas', fontsize = 10)
		axs[0].set_xlabel('')
		axs[0].set_ylabel('')
		axs[0].tick_params(axis = 'x', labelsize = 8)
		axs[0].tick_params(axis = 'y', labelsize = 8)


		conteo_grupos = df['GRUPO'].value_counts()
		axs[1].grid(True, linestyle = '--', alpha = 0.5)
		sns.barplot(x=conteo_grupos.values, y=conteo_grupos.index, ax = axs[1], color = 'royalblue')

		# Agregar etiquetas y título
		axs[1].set_title('Cantidad de individuos por grupo', fontsize = 10)
		axs[1].set_xlabel('')
		axs[1].set_ylabel('')
		axs[1].tick_params(axis = 'x', labelsize = 8)
		axs[1].tick_params(axis = 'y', labelsize = 8)

		
		data_grouped = df.groupby('PROF/m').agg({'Camaron/kg': 'sum', 'FAC/kg': 'sum'}).reset_index()
		axs[2].grid(True, linestyle = '--', alpha = 0.5)
		sns.barplot(x='PROF/m', y='FAC/kg', data=data_grouped, color='royalblue', label='FAC/kg', ax = axs[2])
		sns.barplot(x='PROF/m', y='Camaron/kg', data=data_grouped, color='lightpink', label='Camaron/kg', ax = axs[2])

		#Agregar leyendas y etiquetas
		axs[2].set_title('KG de camarón y FAC capturado por profundidad', fontsize = 10)
		axs[2].set_xlabel('')
		axs[2].set_ylabel('')
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
		sns.lineplot(x=df_resampled.index, y=df_resampled.values, data=df_resampled, ax = axs[3], color = 'royalblue')
		unique_dates = df_resampled.index

		# Agregar etiquetas y título
		axs[3].set_title('Total de individuos capturadas por día', fontsize = 10)
		axs[3].set_xlabel('')
		axs[3].set_ylabel('')
		axs[3].tick_params(axis = 'x', labelsize = 8)
		axs[3].tick_params(axis = 'y', labelsize = 8)
		axs[3].set_xticks(unique_dates)
		axs[3].set_xticklabels([date.strftime('%d/%m/%Y') for date in unique_dates], rotation=90, ha='right')

		plt.tight_layout()

		return fig

	def createPlots2(self, df):
		# Crear los datos y generar la gráfica usando Seaborn
		fig, axs = plt.subplots(4, figsize=(9, 16), facecolor='none')

		axs[0].pie(df['DIA/NOCHE'].value_counts(), labels=df['DIA/NOCHE'].value_counts().index, autopct='%1.1f%%', colors=['skyblue', 'lightcoral'])
		axs[0].set_title('Porcentaje de lances de día y de noche', fontsize = 10)
		labels = df['DIA/NOCHE'].unique()

		etiquetas_personalizadas = {1: 'Hembra', 2: 'Macho', 3: 'Indeterminado'}
		etiquetas = df['SEXO'].map(etiquetas_personalizadas)
		axs[1].pie(etiquetas.value_counts(), labels=etiquetas.value_counts().index, autopct='%1.1f%%', colors=['skyblue', 'lightcoral', 'blueviolet'])
		axs[1].set_title('Porcentaje de sexos', fontsize = 10)
		
		sns.boxplot(x='LONG_TOT', data=df, ax = axs[2])
		axs[2].set_title('Distribución de longitud de especies en milimetros', fontsize = 10)
		axs[2].set_xlabel('')
		axs[2].set_ylabel('')

		sns.boxplot(x='PESO', data=df, ax = axs[3])
		axs[3].set_title('Distribución de peso de especies en gramos', fontsize = 10)
		axs[3].set_xlabel('')
		axs[3].set_ylabel('')

		plt.tight_layout()

		return fig
	
	def filter_dashboard_data(self, df_list):
		try:
			self.fig_captures = self.createPlots(df_list)
			self.fig_species = self.createPlots2(df_list)
			
			self.tabs.delete('Lances')
			self.tabs.add('Lances')
			self.dashboard_captures_frame = ctk.CTkScrollableFrame(self.tabs.tab('Lances'))
			self.dashboard_captures_frame.pack(fill='both', expand=True)

			self.canvas_captures = FigureCanvasTkAgg(self.fig_captures, master = self.dashboard_captures_frame)
			self.canvas_captures.draw()
			self.canvas_captures.get_tk_widget().configure(highlightthickness = 0)
			self.canvas_captures.get_tk_widget().pack(fill='both', expand=True)

			toolbar = NavigationToolbar2Tk(self.canvas_captures, self.dashboard_captures_frame)
			toolbar.update()
			toolbar.pack()
			
			self.tabs.delete('Especies')
			self.tabs.add('Especies')
			self.dashboard_species_frame = ctk.CTkScrollableFrame(self.tabs.tab('Especies'))
			self.dashboard_species_frame.pack(fill='both', expand=True)

			self.canvas_species = FigureCanvasTkAgg(self.fig_species, master = self.dashboard_species_frame)
			self.canvas_species.draw()
			self.canvas_species.get_tk_widget().configure(highlightthickness = 0)
			self.canvas_species.get_tk_widget().pack(fill='both', expand=True)

			toolbar2 = NavigationToolbar2Tk(self.canvas_species, self.dashboard_species_frame)
			toolbar2.update()
			toolbar2.pack()
			
		except Exception as e:
			CTkMessagebox(title = 'Error', message = f'Error inesperado: {str(e)}', icon = 'warning')
			return