import customtkinter as ctk
import seaborn as sns
import pandas as pd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Widgets.style import Estilo
import matplotlib.pyplot as plt
from dataframe import Data
from datetime import datetime

class captures(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		estilo = Estilo()
		self.grid(sticky= 'nswe')
		self.grid_columnconfigure(1, weight = 1)
		self.grid_rowconfigure(0, weight = 1)

		self.infoFrame = ctk.CTkScrollableFrame(self)
		self.infoFrame.configure(corner_radius = 5, scrollbar_button_hover_color = ('gray86', 'gray17'), scrollbar_button_color = ('gray81', 'gray20'))
		self.infoFrame.grid(row = 0, column = 0, sticky = 'nwse', padx = 8, pady = 8)
		self.infoFrame.grid_rowconfigure(6, weight = 1)
		self.infoFrame.grid_columnconfigure(0, weight = 1)
		
		self.infoLabel = ctk.CTkLabel(self.infoFrame, text = 'Filtros', font = ctk.CTkFont(size = 15, weight = 'bold'))
		self.infoLabel.grid(row = 0, column = 0, padx = 20, pady = 20)
		
		self.Label_Project = ctk.CTkLabel(self.infoFrame, text = 'Proyecto:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.OptionMenu_Project = ctk.CTkOptionMenu(self.infoFrame, values = sorted([str(valor) for valor in Data.dataframe['PROYECTO/SIP'].unique().tolist()]), dynamic_resizing = False)
		self.Label_Project.grid(row = 1, column = 0, sticky = 'w')
		self.OptionMenu_Project.grid(row = 2, column = 0, padx = 2, pady = 2, sticky = 'ew')

		self.Label_Year = ctk.CTkLabel(self.infoFrame, text = 'Año:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.OptionMenu_Year = ctk.CTkOptionMenu(self.infoFrame, values = sorted([str(valor) for valor in Data.dataframe['AÑO'].unique().tolist()]), dynamic_resizing = False)
		self.Label_Year.grid(row = 3, column = 0, sticky = 'w')
		self.OptionMenu_Year.grid(row = 4, column = 0, padx = 2, pady = 2, sticky = 'ew')
		
		Data.dataframe['FECHA'] = pd.to_datetime(Data.dataframe['FECHA'], unit='s')
		fechas_formateadas = Data.dataframe['FECHA'].dt.strftime('%d/%m/%Y').tolist()
		fechas_unicas = pd.Series(fechas_formateadas).unique().tolist()	
		self.Label_Date = ctk.CTkLabel(self.infoFrame, text = 'Fecha:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.OptionMenu_Date = ctk.CTkOptionMenu(self.infoFrame, values = fechas_unicas, dynamic_resizing = False)
		self.Label_Date.grid(row = 5, column = 0, sticky = 'w')
		self.OptionMenu_Date.grid(row = 6, column = 0, padx = 2, pady = 2, sticky = 'ew')
			
		self.Label_Area = ctk.CTkLabel(self.infoFrame, text = 'Área:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.OptionMenu_Area = ctk.CTkOptionMenu(self.infoFrame, values = sorted([str(valor) for valor in Data.dataframe['AREA'].unique().tolist()]), dynamic_resizing = False)
		self.Label_Area.grid(row = 7, column = 0, sticky = 'w')
		self.OptionMenu_Area.grid(row = 8, column = 0, padx = 2, pady = 2, sticky = 'ew')
			
		self.Label_Reg = ctk.CTkLabel(self.infoFrame, text = 'Región:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.OptionMenu_Reg = ctk.CTkOptionMenu(self.infoFrame, values = sorted([str(valor) for valor in Data.dataframe['REGION'].unique().tolist()]), dynamic_resizing = False)
		self.Label_Reg.grid(row = 9, column = 0, sticky = 'w')
		self.OptionMenu_Reg.grid(row = 10, column = 0, padx = 2, pady = 2, sticky = 'ew')
			
		self.Label_Reg = ctk.CTkLabel(self.infoFrame, text = 'Subzona:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.OptionMenu_Reg = ctk.CTkOptionMenu(self.infoFrame, values = sorted([str(valor) for valor in Data.dataframe['SUBZONA'].unique().tolist()]), dynamic_resizing = False)
		self.Label_Reg.grid(row = 11, column = 0, sticky = 'w')
		self.OptionMenu_Reg.grid(row = 12, column = 0, padx = 2, pady = 2, sticky = 'ew')

		self.Button = ctk.CTkButton(self, text = 'Aplicar filtros')
		self.Button.grid(row = 1, column = 0, sticky = 'ew', padx = 8, pady = (2, 8))

		self.Dashboard_Frame = ctk.CTkFrame(self)
		self.Dashboard_Frame.grid(row = 0, column = 1, rowspan = 2, sticky = 'nsew', padx = 8, pady = 8)

		# Crear los datos y generar la gráfica usando Seaborn
		fig, axs = plt.subplots(2, 2, figsize=(12, 7), facecolor='none')
		plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.3)

		data_grouped = Data.dataframe.groupby('PROF/m').agg({'Camaron/kg': 'sum', 'FAC/kg': 'sum'}).reset_index()

		plt.figure(figsize=(10, 6))
		sns.barplot(x='PROF/m', y='FAC/kg', data=data_grouped, color='orange', label='FAC/kg', ax = axs[0, 0])
		sns.barplot(x='PROF/m', y='Camaron/kg', data=data_grouped, color='blue', label='Camaron/kg', ax = axs[0, 0])

		# Agregar leyendas y etiquetas
		axs[0, 0].set_xlabel('PROF/m')
		axs[0, 0].set_ylabel('Total')
		axs[0, 0].set_title('Total de Camaron/kg y FAC/kg por PROF/m')
		lines, labels = axs[0, 0].get_legend_handles_labels()
		axs[0, 0].legend(lines, labels)

		conteo_especies = Data.dataframe['ESPECIE'].value_counts()
		conteo_especies_top20 = conteo_especies.head(10)
		sns.barplot(x=conteo_especies_top20.index, y=conteo_especies_top20.values, ax = axs[0, 1])
		# Agregar etiquetas y título
		axs[0, 1].set_xlabel('Especie')
		axs[0, 1].set_ylabel('Cantidad Capturada')
		axs[0, 1].set_title('Conteo de Especies Capturadas')

		# Rotar las etiquetas del eje x para que sean legibles si hay muchas especies
		axs[0, 1].set_xticklabels(axs[0, 1].get_xticklabels(), rotation=90)

		conteo_grupos = Data.dataframe['GRUPO'].value_counts()

		# Crear la gráfica de barra
		sns.barplot(x=conteo_grupos.index, y=conteo_grupos.values, ax = axs[1, 0])

		# Agregar etiquetas y título
		axs[1, 0].set_xlabel('Grupo')
		axs[1, 0].set_ylabel('Cantidad de Especies')
		axs[1, 0].set_title('Cantidad de Especies por Grupo')

		# Rotar las etiquetas del eje x para que sean legibles
		axs[1, 0].set_xticklabels(axs[1, 0].get_xticklabels(), rotation=90)

		Data.dataframe['FECHA'] = pd.to_datetime(Data.dataframe['FECHA'])  # Convertir la columna FECHA a tipo datetime si no lo está
		df_resampled = Data.dataframe.resample('D', on='FECHA').sum(numeric_only = True)  # Resampleo de datos mensuales, si es anual, usa 'Y'
		sns.lineplot(x=df_resampled.index, y='Nºind/Tot', data=df_resampled, ax = axs[1, 1])
		axs[1, 1].set_xlabel('Fecha')
		axs[1, 1].set_ylabel('Captura Total')
		axs[1, 1].set_title('Tendencia Temporal de la Captura Total por Mes')
		plt.tight_layout()

		# Crear el lienzo de la gráfica y agregarlo al marco
		canvas = FigureCanvasTkAgg(fig, master = self.Dashboard_Frame)
		canvas.draw()
		canvas.get_tk_widget().configure(bg = 'lightgray', highlightthickness = 0)
		canvas.get_tk_widget().pack()