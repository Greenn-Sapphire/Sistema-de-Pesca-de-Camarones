import matplotlib.pyplot as plt
import customtkinter as ctk
import seaborn as sns
import pandas as pd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from Widgets.filterpanel import FilterPanel
from CTkMessagebox import CTkMessagebox

class captures(ctk.CTkFrame):
	def __init__(self, master, dataframe):
		super().__init__(master)
		self.grid_remove()
		self.grid(sticky= 'nswe')
		self.grid_columnconfigure(1, weight = 1)
		self.grid_rowconfigure(0, weight = 1)
		self.dataframe = dataframe
		
		nonfilterlist = ['LAT_INI', 'LONG_INI', 'LAT_FIN', 'LONG_FIN', 'LAT_INI', 'Nºind/Tot', 
				   'Nºind/mes', 'Nºind/est', 'LONG_TOT', 'LONG_PAT', 'DIAME_DISCO', 'PESO', 'WA',
				   'CLAV_GRUP', 'CLA_ORDEN', 'CLAVE_FAM', 'CLAVE_SP', 'OBSERV']

		self.filterFrame = FilterPanel(self, self.dataframe, nonfilterlist, width = 150)
		self.filterFrame.configure(corner_radius = 5)
		self.filterFrame.grid(row = 0, column = 0, sticky = 'nwse', padx = 8, pady = 8)
		self.filterFrame.grid_rowconfigure(8, weight = 1)
		self.filterFrame.grid_columnconfigure(0, weight = 1)

		self.Button = ctk.CTkButton(self, text = 'Aplicar filtros', command = self.Filter_callbck)
		self.Button.grid(row = 1, column = 0, sticky = 'ew', padx = 8, pady = (2, 8))

		self.Dashboard_Frame = ctk.CTkScrollableFrame(self)
		self.Dashboard_Frame.grid(row = 0, column = 1, rowspan = 2, sticky = 'nsew', padx = 8, pady = 8)

		fig = self.createPlots(self.dataframe)

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
		axs[0].set_title('Conteo de las primeras 20 especies más capturadas', fontsize = 10)
		axs[0].set_xlabel('')
		axs[0].set_ylabel('')
		axs[0].tick_params(axis = 'x', labelsize = 8)
		axs[0].tick_params(axis = 'y', labelsize = 8)


		conteo_grupos = df['GRUPO'].value_counts()
		axs[1].grid(True, linestyle = '--', alpha = 0.5)
		sns.barplot(x=conteo_grupos.values, y=conteo_grupos.index, ax = axs[1])

		# Agregar etiquetas y título
		axs[1].set_title('Cantidad de individuos por grupo', fontsize = 10)
		axs[1].set_xlabel('')
		axs[1].set_ylabel('')
		axs[1].tick_params(axis = 'x', labelsize = 8)
		axs[1].tick_params(axis = 'y', labelsize = 8)

		
		data_grouped = df.groupby('PROF/m').agg({'Camaron/kg': 'sum', 'FAC/kg': 'sum'}).reset_index()
		axs[2].grid(True, linestyle = '--', alpha = 0.5)
		sns.barplot(x='PROF/m', y='FAC/kg', data=data_grouped, color='orange', label='FAC/kg', ax = axs[2])
		sns.barplot(x='PROF/m', y='Camaron/kg', data=data_grouped, color='blue', label='Camaron/kg', ax = axs[2])

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
		sns.lineplot(x=df_resampled.index, y=df_resampled.values, data=df_resampled, ax = axs[3])

		# Agregar etiquetas y título
		axs[3].set_title('Total de especies capturadas por día', fontsize = 10)
		axs[3].set_xlabel('')
		axs[3].set_ylabel('')
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

			df_list = self.filterFrame.apply_filter_graphs()
		
			fig = self.createPlots(df_list)

			self.canvas = FigureCanvasTkAgg(fig, master = self.Dashboard_Frame)
			self.canvas.draw()
			self.canvas.get_tk_widget().configure(bg = 'lightgray', highlightthickness = 0)
			self.canvas.get_tk_widget().pack()

			toolbar = NavigationToolbar2Tk(self.canvas, self.Dashboard_Frame)
			toolbar.update()
			toolbar.pack()
		except Exception as e:
			CTkMessagebox(title = 'Error', message = f'Error inesperado: {str(e)}', icon = 'warning')
			return