import matplotlib.pyplot as plt
import customtkinter as ctk
import seaborn as sns

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from Widgets.filterpanel import FilterPanel
from CTkMessagebox import CTkMessagebox

class species(ctk.CTkFrame):
	def __init__(self, master, dataframe):
		super().__init__(master)
		self.grid_remove()
		self.grid(sticky= 'nswe')
		self.grid_columnconfigure(1, weight = 1)
		self.grid_rowconfigure(0, weight = 1)
		self.dataframe = dataframe		
		
		nonfilterlist = ['LAT_INI', 'LONG_INI', 'LAT_FIN', 'LONG_FIN', 'LAT_INI', 'Hr_INI', 'Hr_FIN', 'Nºind/Tot', 
				   'Nºind/mes', 'Nºind/est', 'CLAV_GRUP', 'CLA_ORDEN', 'CLAVE_FAM', 'CODIGOSPP', 'CLAVE_SP', 'OBSERV']

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
		axs[2].set_title('Distribución de longitud de especies en milimetros', fontsize = 10)
		axs[2].set_xlabel('')
		axs[2].set_ylabel('')

		sns.boxplot(x='PESO', data=df, ax = axs[3])
		axs[3].set_title('Distribución de peso de especies en gramos', fontsize = 10)
		axs[3].set_xlabel('')
		axs[3].set_ylabel('')

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