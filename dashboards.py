import matplotlib.pyplot as plt
import customtkinter as ctk
import seaborn as sns
import pandas as pd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.gridspec import GridSpec
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
		
		self.toolbar = NavigationToolbar2Tk(self.canvas_captures, self.dashboard_captures_frame)
		self.toolbar.update()
		self.toolbar.pack()
		
		self.fig_species = self.createPlots2(self.dataframe)
		
		self.canvas_species = FigureCanvasTkAgg(self.fig_species, master = self.dashboard_species_frame)
		self.canvas_species.draw()
		self.canvas_species.get_tk_widget().configure(highlightthickness = 0)
		self.canvas_species.get_tk_widget().pack(fill='both', expand=True)
		
		self.toolbar2 = NavigationToolbar2Tk(self.canvas_species, self.dashboard_species_frame)
		self.toolbar2.update()
		self.toolbar2.pack()

	def createPlots(self, df):
		# Crear los datos y generar la gráfica usando Seaborn
		fig = plt.figure(figsize=(9, 16), facecolor='none')
		gs = GridSpec(4, 2, figure=fig)

		# PRIMER GRAFICA
		ax0 = fig.add_subplot(gs[0, :])
		conteo_especies = df['ESPECIE'].value_counts()
		conteo_especies_top20 = conteo_especies.head(20)
		sns.barplot(x=conteo_especies_top20.values, y=conteo_especies_top20.index, ax = ax0, color = 'royalblue')

		# Agregar etiquetas y título
		ax0.set_title('Conteo de las primeras 20 especies más capturadas', fontsize = 10)
		ax0.set_xlabel('')
		ax0.set_ylabel('')
		ax0.tick_params(axis = 'x', labelsize = 8)
		ax0.tick_params(axis = 'y', labelsize = 8)

		# SEGUNDA GRAFICA
		ax1 = fig.add_subplot(gs[1, :])
		conteo_grupos = df['GRUPO'].value_counts()
		#ax1.grid(True, linestyle = '--', alpha = 0.5)
		sns.barplot(x=conteo_grupos.values, y=conteo_grupos.index, ax = ax1, color = 'royalblue')

		# Agregar etiquetas y título
		ax1.set_title('Cantidad de individuos por grupo', fontsize = 10)
		ax1.set_xlabel('')
		ax1.set_ylabel('')
		ax1.tick_params(axis = 'x', labelsize = 8)
		ax1.tick_params(axis = 'y', labelsize = 8)

		# TERCER GRAFICA
		data_grouped = df.groupby('PROF/m').agg({'Camaron/kg': 'sum', 'FAC/kg': 'sum'}).reset_index()
		ax2 = fig.add_subplot(gs[2, 0])
		#sns.histplot(data_grouped['FAC/kg'], bins=6, edgecolor='black', color='royalblue', label='FAC/kg', ax = ax2)
		sns.scatterplot(x='PROF/m', y='FAC/kg', data=df, color='royalblue', ax = ax2)

		#Agregar leyendas y etiquetas
		ax2.set_title('KG de FAC capturado por profundidad', fontsize = 10)
		#ax2.set_xlabel('')
		#ax2.set_ylabel('')
		ax2.tick_params(axis='both', labelsize=8)
		
		ax3 = fig.add_subplot(gs[2, 1])
		#sns.histplot(data_grouped['Camaron/kg'], bins=bins, edgecolor='black', color='hotpink', label='Camaron/kg', ax = ax3)
		sns.scatterplot(x='PROF/m', y='Camaron/kg', data=df, color='hotpink', ax = ax3)

		#Agregar leyendas y etiquetas
		ax3.set_title('KG de camarón capturado por profundidad', fontsize = 10)
		#ax3.set_xlabel('')
		#ax3.set_ylabel('')
		ax3.tick_params(axis='both', labelsize=8)

		# CUARTA GRAFICA
		ax4 = fig.add_subplot(gs[3, :])
		df_resampled = df.copy()
		df_resampled['FECHA'] = pd.to_datetime(df_resampled['FECHA'], format='%d/%m/%Y')
		df_resampled.set_index('FECHA', inplace=True)
		df_resampled = df_resampled.resample('D')['ESPECIE'].count()
		sns.lineplot(x=df_resampled.index.strftime('%d/%m/%Y'), y=df_resampled.values, ax=ax4, color='royalblue')

		# Agregar etiquetas y título
		ax4.set_title('Total de individuos capturados por día', fontsize=10)
		ax4.set_xlabel('')
		ax4.set_ylabel('')
		ax4.tick_params(axis='x', labelsize=8, rotation=90)
		ax4.tick_params(axis='y', labelsize=8)

		plt.tight_layout()

		return fig

	def createPlots2(self, df):
		# Crear los datos y generar la gráfica usando Seaborn
		fig = plt.figure(figsize=(9, 16), facecolor='none')
		gs = GridSpec(5, 2, figure=fig)

		# PRIMER GRAFICA
		ax0 = fig.add_subplot(gs[0, 0])
		ax0.pie(df['DIA/NOCHE'].value_counts(), labels=df['DIA/NOCHE'].value_counts().index, autopct='%1.1f%%', colors=['royalblue', 'hotpink'])
		ax0.set_title('Porcentaje de individuos capturados de día y noche', fontsize = 10)

		# SEGUNDA GRAFICA
		ax1 = fig.add_subplot(gs[0, 1])
		etiquetas_personalizadas = {1: 'Hembra', 2: 'Macho', 3: 'Indeterminado'}
		etiquetas = df['SEXO'].map(etiquetas_personalizadas)
		ax1.pie(etiquetas.value_counts(), labels=etiquetas.value_counts().index, autopct='%1.1f%%', colors=['silver', 'royalblue', 'hotpink'])
		ax1.set_title('Porcentaje de individuos pertenecientes a cada sexo', fontsize = 10)

		# TERCER GRAFICA
		ax2 = fig.add_subplot(gs[1, :])
		sns.boxplot(x='LONG_TOT', data=df, ax = ax2, color = 'royalblue')
		ax2.set_title('Distribución de longitud de especie en milimetros', fontsize = 10)
		ax2.set_xlabel('')
		ax2.set_ylabel('')

		ax4 = fig.add_subplot(gs[2, :])
		ax4.hist(x='LONG_TOT', data=df, bins=8, edgecolor='black', color = 'royalblue')  # Ajusta el número de bins según tus datos
		ax4.set_title('Histograma de longitud total', fontsize = 10)
		ax4.set_xlabel('')
		ax4.set_ylabel('')

		# CUARTA GRAFICA
		ax4 = fig.add_subplot(gs[3, :])
		sns.boxplot(x='PESO', data=df, ax = ax4, color = 'royalblue')
		ax4.set_title('Distribución de peso de especie en gramos', fontsize = 10)
		ax4.set_xlabel('')
		ax4.set_ylabel('')

		ax5 = fig.add_subplot(gs[4, :])
		ax5.hist(x='PESO', data=df, bins=8, edgecolor='black', color = 'royalblue')  # Ajusta el número de bins según tus datos
		ax5.set_title('Histograma del peso', fontsize = 10)
		ax5.set_xlabel('')
		ax5.set_ylabel('')

		plt.tight_layout()

		return fig
	
	def filter_dashboard_data(self, df_list):
		try:
			self.fig_captures = self.createPlots(df_list)

			self.canvas_captures.get_tk_widget().destroy()
			self.toolbar.destroy()
			self.canvas_captures = FigureCanvasTkAgg(self.fig_captures, master = self.dashboard_captures_frame)
			self.canvas_captures.draw()
			self.canvas_captures.get_tk_widget().configure(highlightthickness = 0)
			self.canvas_captures.get_tk_widget().pack(fill='both', expand=True)

			self.toolbar = NavigationToolbar2Tk(self.canvas_captures, self.dashboard_captures_frame)
			self.toolbar.update()
			self.toolbar.pack()

		except Exception as e:
			CTkMessagebox(title = 'Error', message = f'Error inesperado: {str(e)}\n\nRevisa los datos filtrados.', icon = 'warning')
			raise
			
		try:
			self.fig_species = self.createPlots2(df_list)

			self.canvas_species.get_tk_widget().destroy()
			self.toolbar2.destroy()
			self.canvas_species = FigureCanvasTkAgg(self.fig_species, master = self.dashboard_species_frame)
			self.canvas_species.draw()
			self.canvas_species.get_tk_widget().configure(highlightthickness = 0)
			self.canvas_species.get_tk_widget().pack(fill='both', expand=True)

			self.toolbar2 = NavigationToolbar2Tk(self.canvas_species, self.dashboard_species_frame)
			self.toolbar2.update()
			self.toolbar2.pack()
			
		except Exception as e:
			CTkMessagebox(title = 'Error', message = f'Error inesperado: {str(e)}\n\nRevisa los datos filtrados.', icon = 'warning')
			raise